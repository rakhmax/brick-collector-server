from server.src.api.Themes import Themes
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from zeep import Client
import os

app = Flask(__name__)
CORS(app)
api = Api(app)

from .api.Minifigs import Minifigs
from .api.Search import Search

app.config['SECRET_KEY'] = os.urandom(12)

api.add_resource(Minifigs, '/minifigs')
api.add_resource(Search, '/search')
api.add_resource(Themes, '/themes')

if __name__ == '__main__':
    app.run()
