from flask import request
from flask_restful import Resource
from bson.json_util import loads
from ..db import db

class Minifigs(Resource):
    def get(self):
        minifigs = list(db.minifigures.aggregate([
            {'$group' : {
                '_id': '$number',
                'legoId': {'$first': '$legoId'},
                'img': {'$first': '$img'},
                'name': {'$first': '$name'},
                'price': {'$first': '$price'},
                'theme': {'$first': '$theme'},
                'number': {'$first': '$number'},
                'comment': {'$first': '$comment'},
                'count': { '$sum': 1 }
            }},
            {'$project': {'_id': 0}}
        ]))

        return minifigs

    def post(self):
        data = loads(request.data)

        try:
            minifigure = db.minifigures.insert_one(data)

            return db.minifigures.find_one({ '_id': minifigure.inserted_id }, { '_id': 0 })
        except Exception as e:
            if e.code == 11000:
                return { 'error': { 'message': 'Already in the collection' }}, 503
