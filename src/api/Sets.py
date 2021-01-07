import html
from bricklink_api.catalog_item import get_item, get_subsets, Type
from bson.json_util import loads
from bson.objectid import ObjectId
from flask import current_app, request
from flask_restful import Resource
from pymongo.collection import ReturnDocument
from src.helpers.clearNullItems import cleanNullTerms
from src.db import db


class Sets(Resource):
    mf_col = db.minifigures
    s_col = db.sets

    def get(self):
        try:
            sets = list(self.s_col.aggregate([
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

            total = self.s_col.count_documents({})

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

            json_sets = get_item(
                Type.SET,
                data['itemId'],
                auth=current_app.config['BRICKLINK_AUTH'])

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
                auth=current_app.config['BRICKLINK_AUTH'])

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
                        auth=current_app.config['BRICKLINK_AUTH'])

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

            set_data = {
                'itemId': bricklink_data['no'],
                'name': html.unescape(bricklink_data['name']),
                'categoryId': bricklink_data['category_id'],
                'image': {
                    'base': bricklink_data['image_url'],
                    'thumbnail': bricklink_data['thumbnail_url']
                },
                'year': bricklink_data['year_released'],
                'minifigures': [minifigure['_id'] for minifigure in minifigures],
                'price': float(data['price']) if data['price'] else None,
                'comment': data['comment'],
                'sealed': data['sealed'],
                'pieces': pieces,
                'extraPieces': extra_pieces
            }

            inserted_set = self.s_col.insert_one(set_data).inserted_id

            if minifigures:
                self.mf_col.insert_many(minifigures, ordered=False)

            mf = []

            for minifig in minifigures:
                del minifig['_id']
                mf.append(minifig)

            inserted_set = self.s_col.find_one({ '_id': inserted_set }, { '_id': 0 })
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

            updated_set = self.s_col.find_one_and_update(
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
            lego_id = data['itemId']
            with_minifigures = data['withMinifigures']

            deleted_set = self.s_col.find_one_and_delete({ 'itemId': lego_id }, { '_id': 0 })

            if with_minifigures:
                self.mf_col.delete_many({ '_id': { '$in': deleted_set['minifigures'] } })

            del deleted_set['minifigures']

            return deleted_set
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500
