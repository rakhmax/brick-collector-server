import requests
from flask_restful import Resource
from ..const import rebrickableApiKey, rebrickableApiUrl


class Themes(Resource):
    def get(self):
        themes = requests.get(f'{rebrickableApiUrl}/themes/?key={rebrickableApiKey}&page_size=1000').json()
        filtered_themes = [theme for theme in themes['results'] if theme['parent_id'] == None]

        return filtered_themes
