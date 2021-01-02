import re
import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
from ..const import rebrickableSearchUrl


class Search(Resource):
    def get(self):
        try:
            query = request.args['query']

            response = requests.get(f'{rebrickableSearchUrl}/?q={query}').json()

            result = []

            for item in response:
                soup = BeautifulSoup(item['name'], 'lxml')
                image = soup.find('img')

                id = item['id']
                img = image['src']
                n = image.next_element.replace(id, '')
                year = re.search(r'\((\d+)\)', n).groups()[0] or None
                name = n.replace(f'({year})', '')

                result.append({
                    'id': id,
                    'name': name.strip(),
                    'year': year,
                    'img': img,
                })

            return result
        except Exception as e:
            print(e)
