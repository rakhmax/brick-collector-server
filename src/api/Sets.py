import html
from bricklink_api.catalog_item import get_item, get_subsets, Type
from bson.json_util import loads
from bson.objectid import ObjectId
from flask import current_app, request
from flask_restful import Resource
from ..db import db


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
                    'minifiguresCount': { '$size': '$minifigures' }
                }}
            ]))

            return sets
        except Exception as e:
            print(e)

    def post(self):
        try:
            data = loads(request.data)

            json_sets = get_item(
                Type.SET,
                data['id'],
                auth=current_app.config['BRICKLINK_AUTH'])

            bricklink_data = json_sets['data']

            if not bricklink_data:
                raise Exception('No item with the ID')

            bricklink_parts_data = get_subsets(
                Type.SET,
                data['id'],
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
                'minifigures': [minifigure['itemId'] for minifigure in minifigures],
                'price': data['price'],
                'comment': data['comment'],
                'pieces': pieces,
                'extraPieces': extra_pieces
            }

            inserted_set = self.s_col.insert_one(set_data).inserted_id
            self.mf_col.insert_many(minifigures, ordered=False)

            mf = []

            for minifig in minifigures:
                del minifig['_id']
                mf.append(minifig)

            return {
                'minifigures': mf,
                'set': self.s_col.find_one({ '_id': inserted_set }, { '_id': 0 })
            }
        except Exception as e:
            print(e)

    def delete(self):
        try:
            lego_id = request.data.decode('utf-8')
            return self.s_col.find_one_and_delete({ 'itemId': lego_id }, { '_id': 0 })
        except Exception as e:
            print(e)
