import html
from bricklink_api.catalog_item import get_item, Type
from bson.json_util import loads
from flask import current_app, request
from flask_restful import Resource
from ..db import db


class Minifigs(Resource):
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

            return minifigs
        except Exception as e:
            print(e)

    def post(self):
        try:
            data = loads(request.data)

            json = get_item(
                Type.MINIFIG,
                data['id'],
                auth=current_app.config['BRICKLINK_AUTH'])

            bricklink_data = json['data']

            if not bricklink_data:
                raise Exception('No items with the ID')

            minifig = {
                'itemId': bricklink_data['no'],
                'name': html.unescape(bricklink_data['name']),
                'categoryId': bricklink_data['category_id'],
                'image': {
                    'base': bricklink_data['image_url'],
                    'thumbnail': bricklink_data['thumbnail_url']
                },
                'year': bricklink_data['year_released'],
                'price': data['price'],
                'comment': data['comment']
            }

            minifigure = self.mf_col.insert_one(minifig)

            return self.mf_col.find_one({ '_id': minifigure.inserted_id }, { '_id': 0 })
        except Exception as e:
            print(e)

    def delete(self):
        try:
            lego_id = request.data.decode('utf-8')
            return self.mf_col.find_one_and_delete({ 'itemId': lego_id }, { '_id': 0 })
        except Exception as e:
            print(e)
