import html
from bricklink_api.catalog_item import get_item, get_subsets, Type
from bson.json_util import loads
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource
from pymongo.collection import ReturnDocument
from src.app import auth
from src.db import db


class Sets(Resource):
    def get(self):
        try:
            access_string = request.headers.get('Authorization')
            s_user_col = db[f's{access_string}']

            sets = list(s_user_col.aggregate([
                {'$group' : {
                    '_id': '$itemId',
                    'itemId': {'$first': '$itemId'},
                    'image': {'$first': '$image'},
                    'name': {'$first': '$name'},
                    'price': {'$first': '$price'},
                    'categoryId': {'$first': '$categoryId'},
                    'comment': {'$first': '$comment'},
                    'year': {'$first': '$year'},
                    'minifigures': {'$first': '$minifigures'},
                    'pieces': {'$first': '$pieces'},
                    'extraPieces': {'$first': '$extraPieces'},
                    'sealed': {'$first': '$sealed'},
                    'count': { '$sum': 1 }
                }},
                {'$project': {
                    '_id': 0, 
                    'itemId': 1,
                    'image': 1,
                    'name': 1,
                    'price': 1,
                    'categoryId': 1,
                    'comment': 1,
                    'year': 1,
                    'count': 1,
                    'pieces': 1,
                    'extraPieces': 1,
                    'sealed': 1,
                    'minifiguresCount': { '$size': '$minifigures' }
                }}
            ]))

            total = s_user_col.count_documents({})

            return {
                'sets': sets,
                'total': total
            }
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500

    def post(self):
        try:
            data = loads(request.data)
            access_string = request.headers.get('Authorization')
            mf_user_col = db[f'mf{access_string}']
            s_user_col = db[f's{access_string}']

            json_sets = get_item(
                Type.SET,
                data['itemId'],
                auth=auth)

            if json_sets['meta']['code'] == 400:
                raise Exception('No item with the ID')

            bricklink_data = json_sets['data']

            if not bricklink_data:
                raise Exception('No item with the ID')

            bricklink_parts_data = get_subsets(
                Type.SET,
                data['itemId'],
                instruction=False,
                box=False,
                break_minifigs=False,
                auth=auth)

            pieces = 0
            extra_pieces = 0
            minifigures = []

            for part in bricklink_parts_data['data']:
                quantity = part['entries'][0]['quantity']
                pieces = pieces + quantity

                extra_quantity = part['entries'][0]['extra_quantity']
                extra_pieces = extra_pieces + extra_quantity
                
                item = part['entries'][0]['item']

                if item['type'] == 'MINIFIG':
                    json_minifigs = get_item(
                        Type.MINIFIG,
                        item['no'], 
                        auth=auth)

                    minifig_data = json_minifigs['data']

                    for _ in range(quantity):
                        minifigures.append({
                            '_id': ObjectId(),
                            'itemId': minifig_data['no'],
                            'name': html.unescape(minifig_data['name']),
                            'categoryId': minifig_data['category_id'],
                            'image': {
                                'base': minifig_data['image_url'],
                                'thumbnail': minifig_data['thumbnail_url']
                            },
                            'year': minifig_data['year_released'],
                            'price': None,
                            'comment': None,
                        })

            mf_ids = [minifigure['_id'] for minifigure in minifigures]

            set_data = {
                'itemId': bricklink_data['no'],
                'name': html.unescape(bricklink_data['name']),
                'categoryId': bricklink_data['category_id'],
                'image': {
                    'base': bricklink_data['image_url'],
                    'thumbnail': bricklink_data['thumbnail_url']
                },
                'year': bricklink_data['year_released'],
                'minifigures': mf_ids,
                'price': float(data['price']) if data['price'] else None,
                'comment': data['comment'],
                'sealed': data['sealed'],
                'pieces': pieces,
                'extraPieces': extra_pieces
            }

            inserted_set = s_user_col.insert_one(set_data).inserted_id

            if minifigures:
                mf_user_col.insert_many(minifigures, ordered=False)

            mf = list(mf_user_col.aggregate([
                {'$match': {'_id': {'$in': mf_ids }}},
                {'$group' : {
                    '_id': '$itemId',
                    'itemId': { '$first': '$itemId' },
                    'image': { '$first': '$image' },
                    'name': { '$first': '$name' },
                    'price': { '$first': '$price' },
                    'categoryId': { '$first': '$categoryId' },
                    'comment': { '$first': '$comment' },
                    'year': { '$first': '$year' },
                    'count': { '$sum': 1 }
                }},
                {'$project': { '_id': 0 }}]))

            inserted_set = s_user_col.find_one({ '_id': inserted_set }, { '_id': 0 })
            inserted_set['minifiguresCount'] = len(inserted_set['minifigures'])
            inserted_set['count'] = 1
            del inserted_set['minifigures']

            return {
                'minifigures': mf,
                'set': inserted_set
            }
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500

    def patch(self):
        try:
            data = loads(request.data)
            access_string = request.headers.get('Authorization')
            s_user_col = db[f's{access_string}']

            updated_set = s_user_col.find_one_and_update(
                { 'itemId': data['itemId'] },
                { '$set': data },
                { '_id': 0 },
                return_document=ReturnDocument.AFTER)

            updated_set['minifiguresCount'] = len(updated_set['minifigures'])
            updated_set['count'] = 1
            del updated_set['minifigures']

            return updated_set
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500

    def delete(self):
        try:
            data = loads(request.data)
            access_string = request.headers.get('Authorization')
            mf_user_col = db[f'mf{access_string}']
            s_user_col = db[f's{access_string}']

            lego_id = data['itemId']
            with_minifigures = data['withMinifigures']

            deleted_set = s_user_col.find_one_and_delete({ 'itemId': lego_id }, { '_id': 0 })

            if with_minifigures:
                mf_user_col.delete_many({ '_id': { '$in': deleted_set['minifigures'] } })

            del deleted_set['minifigures']

            return deleted_set
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500
