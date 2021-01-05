from bricklink_api.catalog_item import get_item, get_subsets, Type
from bson.json_util import loads
from flask import current_app, request
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from ..db import db
import html


class Minifigs(Resource):
    def get(self):
        minifigs = list(db.minifigures.aggregate([
            {'$group' : {
                '_id': '$itemId',
                'itemId': {'$first': '$itemId'},
                'image': {'$first': '$image'},
                'name': {'$first': '$name'},
                'price': {'$first': '$price'},
                'categoryId': {'$first': '$categoryId'},
                'comment': {'$first': '$comment'},
                'count': { '$sum': 1 }
            }},
            {'$project': {'_id': 0}}
        ]))

        return minifigs

    def post(self):
        data = loads(request.data)
        json = get_item(Type.MINIFIG, data['id'], auth=current_app.config['BRICKLINK_AUTH'])
        bricklink_data = json['data']

        try:
            if not bricklink_data:
                raise HTTPException('No items with the ID', 509)

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

            minifigure = db.minifigures.insert_one(minifig)

            return db.minifigures.find_one({ '_id': minifigure.inserted_id }, { '_id': 0 })
        except HTTPException as e:
            return {
                'message': 'Item does not exist',
            }, 509

    def delete(self):
        lego_id = request.data.decode('utf-8')

        try:
            r = db.minifigures.find_one_and_delete({ 'itemId': lego_id }, { '_id': 0 })
            return r
        except Exception as e:
            print(e)
