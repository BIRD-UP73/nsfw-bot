import logging

import requests
from requests import Response

from url.urls import UrlEnum


class Rule34Api:
    url = UrlEnum.RULE34

    base_params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
    }

    def create_api_params(tags: str, page: int = 0, limit: int = 0, json: bool = False):
        return Rule34Api.base_params.update({
            'json': int(json),
            'limit': limit,
            'tags': tags,
            'pid': page
        })

    def send_request(self, params: dict) -> Response:
        logging.info(f'Fetching post, params={params}')

        resp = requests.get(self.url.value.long_url, params)
        resp.raise_for_status()

        return resp
