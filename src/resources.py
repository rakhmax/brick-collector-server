from flask_restful import Api
from src.app import app
from src.api.Minifigures import Minifigures
from src.api.PriceGuide import PriceGuide
from src.api.Sets import Sets
from src.api.Themes import Themes


api = Api(app)

api.add_resource(Minifigures, '/minifigures')
api.add_resource(Sets, '/sets')
api.add_resource(Themes, '/themes')
api.add_resource(PriceGuide, '/price')
