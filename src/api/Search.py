from bson.json_util import loads
from flask import request
from flask_restful import Resource
from requests import post


class Search(Resource):
    def get(self):
        try:
            query = request.args.get('query')
            type = request.args.get('type')

            headers = {
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            }

            search_res = loads(post(f'https://www.bricklink.com/ajax/clone/search/searchproduct.ajax?q={query}&type={type}', headers=headers).content)

            res = []

            if search_res:
                types = search_res['result']['typeList']

                for type in types:
                    items = type['items']

                    for item in items:
                        res.append({
                            'itemId': item['strItemNo'],
                            'name': item['strItemNo'] + ' ' + item['strItemName'],
                            'type': item['typeItem'],
                            'image': 'https://img.bricklink.com/ItemImage/' + item['typeItem'] + 'T/0/' + item['strItemNo'] + '.t1.png'
                        })

            return res
        except Exception as e:
            print(e)
            return [], 500
