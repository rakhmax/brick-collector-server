from bricklink_api.catalog_item import get_price_guide, Type, NewOrUsed, GuideType
from flask import current_app, request
from flask_restful import Resource

class PriceGuide(Resource):
    def get(self):
        item_id = request.args.get('id')
        type = request.args.get('type')

        price_guide_new = get_price_guide(
            type,
            item_id,
            auth=current_app.config['BRICKLINK_AUTH']
        )

        price_guide_used = get_price_guide(
            type,
            item_id,
            new_or_used=NewOrUsed.USED,
            auth=current_app.config['BRICKLINK_AUTH']
        )

        price_guide = {
            'new': {
                'min': round(float(price_guide_new['data']['min_price'])),
                'max': round(float(price_guide_new['data']['max_price'])),
                'avg': round(float(price_guide_new['data']['avg_price'])),
            },
            'used': {
                'min': round(float(price_guide_used['data']['min_price'])),
                'max': round(float(price_guide_used['data']['max_price'])),
                'avg': round(float(price_guide_used['data']['avg_price'])),
            }
        }
        
        return price_guide
