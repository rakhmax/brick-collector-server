from bricklink_api.catalog_item import get_price_guide, NewOrUsed
from flask import request
from flask_restful import Resource
from src.app import auth


class PriceGuide(Resource):
    def get(self):
        item_id = request.args.get('itemId')
        type = request.args.get('type')

        price_guide_new = get_price_guide(
            type,
            item_id,
            auth=auth)

        price_guide_used = get_price_guide(
            type,
            item_id,
            new_or_used=NewOrUsed.USED,
            auth=auth)

        price_guide = {
            'new': {
                'min': round(float(price_guide_new['data']['min_price']), 2),
                'max': round(float(price_guide_new['data']['max_price']), 2),
                'avg': round(float(price_guide_new['data']['avg_price']), 2)
            },
            'used': {
                'min': round(float(price_guide_used['data']['min_price']), 2),
                'max': round(float(price_guide_used['data']['max_price']), 2),
                'avg': round(float(price_guide_used['data']['avg_price']), 2)
            }
        }
        
        return price_guide
