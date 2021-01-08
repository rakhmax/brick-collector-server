from bricklink_api.category import get_category_list
from flask_restful import Resource
from src.app import auth


class Themes(Resource):
    def get(self):
        themes = get_category_list(auth=auth)

        filtered_themes = []

        for theme in themes['data']:
            if theme['parent_id'] == 0:
                filtered_themes.append({
                    'id': theme['category_id'],
                    'name': theme['category_name']
                })

        return filtered_themes
