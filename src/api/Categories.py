from bricklink_api.category import get_category_list
from flask_restful import Resource
from src.app import auth


class Categories(Resource):
    def get(self):
        categories = get_category_list(auth=auth)

        filtered_categories = []

        for category in categories['data']:
            if category['parent_id'] == 0:
                filtered_categories.append({
                    'id': category['category_id'],
                    'name': category['category_name']
                })

        return filtered_categories
