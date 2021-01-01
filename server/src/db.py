from enum import unique
from flask_pymongo import PyMongo
from .app import app

app.config['MONGO_URI'] = 'mongodb+srv://admin:LolliPop50@chat-cluster.z8fp2.mongodb.net/chat-cluster?retryWrites=true'
mongo = PyMongo(app)

db = mongo.db

db.minifigures.create_index('number', unique=True)
