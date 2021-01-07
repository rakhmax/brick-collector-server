import os
from flask_pymongo import PyMongo
from src.app import app

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

db = mongo.db
