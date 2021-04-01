import requests


def json_post_by_id(base_url: str, post_id: int) -> dict:
    url = f'{base_url}/{post_id}.json'
    resp = requests.get(url)

    return resp.json()


def send_json_request(url: str, tags: str, limit: int = 1, page: int = 0) -> dict:
    params = {
        'limit': limit,
        'tags': tags,
        'page': page
    }

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.json()
