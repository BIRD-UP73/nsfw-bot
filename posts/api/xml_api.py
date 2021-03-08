import requests


def get_post_by_id(url, post_id):
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'id': post_id
    }

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

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.text
