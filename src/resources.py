from flask_restful import Api
from .app import app
from .api.Minifigures import Minifigures
from .api.Search import Search
from .api.Themes import Themes
from .api.PriceGuide import PriceGuide
from .api.Sets import Sets


api = Api(app)

api.add_resource(Minifigures, '/minifigures')
api.add_resource(Sets, '/sets')
api.add_resource(Search, '/search')
api.add_resource(Themes, '/themes')
api.add_resource(PriceGuide, '/price')
