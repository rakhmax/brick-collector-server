import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from src.api.Themes import Themes


app = Flask(__name__)
CORS(app)
api = Api(app)


from .api.Minifigs import Minifigs
from .api.Search import Search


app.config['SECRET_KEY'] = os.urandom(12)

api.add_resource(Minifigs, '/minifigs')
api.add_resource(Search, '/search')
api.add_resource(Themes, '/themes')
