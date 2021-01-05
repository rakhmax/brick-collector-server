from bricklink_api.category import get_category_list
from flask import current_app
from flask_restful import Resource


class Themes(Resource):
    def get(self):
        themes = get_category_list(auth=current_app.config['BRICKLINK_AUTH'])

        filtered_themes = []

        for theme in themes['data']:
            if theme['parent_id'] == 0:
                filtered_themes.append({
                    'id': theme['category_id'],
                    'name': theme['category_name']
                })

        return filtered_themes
