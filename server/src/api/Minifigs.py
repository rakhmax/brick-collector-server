from flask import request
from flask_restful import Resource
from bson.json_util import dumps, loads
from ..db import db

class Minifigs(Resource):
    def get(self):
        minifigs = list(db.minifigures.find({}))
        return dumps(minifigs)

    def post(self):
        data = loads(request.data)

        try:
            db.minifigures.insert(data)

            return { 'message': 'success' }, 201
        except Exception as e:
            if e.code == 11000:
                return { 'error': { 'message': 'Already in the collection' }}, 503
