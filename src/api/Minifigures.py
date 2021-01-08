import html
from bricklink_api.catalog_item import get_item, Type
from bson.json_util import loads
from flask import current_app, request
from flask_restful import Resource
from pymongo.collection import ReturnDocument
from src.db import db


class Minifigures(Resource):
    mf_col = db.minifigures

    def get(self):
        try:
            minifigs = list(self.mf_col.aggregate([
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

            total = self.mf_col.count_documents({})

            return {
                'minifigs': minifigs,
                'total': total
            }
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500

    def post(self):
        try:
            data = loads(request.data)

            json_minifigs = get_item(
                Type.MINIFIG,
                data['itemId'],
                auth=current_app.config['BRICKLINK_AUTH'])

            if json_minifigs['meta']['code'] == 400:
                raise Exception('No item with the ID')

            bricklink_data = json_minifigs['data']

            if not bricklink_data:
                raise Exception('No item with the ID')

            minifig = {
                'itemId': bricklink_data['no'],
                'name': html.unescape(bricklink_data['name']),
                'categoryId': bricklink_data['category_id'],
                'image': {
                    'base': bricklink_data['image_url'],
                    'thumbnail': bricklink_data['thumbnail_url']
                },
                'year': bricklink_data['year_released'],
                'price': float(data['price']) if data['price'] else None,
                'comment': data['comment']
            }

            minifigure = self.mf_col.insert_one(minifig)

            return self.mf_col.find_one({ '_id': minifigure.inserted_id }, { '_id': 0 })
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500

    def patch(self):
        try:
            data = loads(request.data)

            updated_minifig = self.mf_col.find_one_and_update(
                { 'itemId': data['itemId'] },
                { '$set': data },
                { '_id': 0 },
                return_document=ReturnDocument.AFTER)

            return updated_minifig
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500

    def delete(self):
        try:
            lego_id = request.data.decode('utf-8')
            return self.mf_col.find_one_and_delete({ 'itemId': lego_id }, { '_id': 0 })
        except Exception as e:
            print(e)
            return {'error': 'err'}, 500
