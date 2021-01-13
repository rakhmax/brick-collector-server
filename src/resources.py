from flask_restful import Api
from src.app import app
from src.api.Categories import Categories
from src.api.Minifigures import Minifigures
from src.api.PriceGuide import PriceGuide
from src.api.Search import Search
from src.api.Sets import Sets


api = Api(app)

api.add_resource(Categories, '/categories')
api.add_resource(Minifigures, '/minifigures')
api.add_resource(PriceGuide, '/price')
api.add_resource(Search, '/search')
api.add_resource(Sets, '/sets')
