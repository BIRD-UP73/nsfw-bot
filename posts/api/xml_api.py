import logging

import requests


def get_post_by_id(url: str, post_id: int) -> str:
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'id': post_id
    }

    logging.info(f'Fetching post with id {post_id} request for url {url}')

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.text


def send_request(url: str, limit: int, tags: str, page: int) -> str:
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'limit': limit,
        'pid': page,
        'tags': tags
    }

    logging.info(f'Fetching post for url={url}, tags={tags}, page={page}, limit={limit}')

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.text
