import logging

import requests

from url.urls import URL, Hypnohub


def get_post_by_id(url: URL, post_id: int) -> str:
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'id': post_id
    }
    params.update(url.api_options)

    logging.info(f'Fetching post with id {post_id} request for url {url}')

    resp = requests.get(url.long_url, params)
    resp.raise_for_status()

    return resp.text


def send_request(url: URL, limit: int, tags: str, page: int) -> str:
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'pig': page,
        'limit': limit,
        'tags': tags
    }

    logging.info(f'Fetching post for url={url}, tags={tags}, page={page}, limit={limit}')

    resp = requests.get(url.long_url, params)
    resp.raise_for_status()

    return resp.text
