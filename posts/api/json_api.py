import requests


def json_post_by_id(base_url: str, post_id: int) -> dict:
    url = f'{base_url}/posts/{post_id}.json'
    resp = requests.get(url)

    return resp.json()


def send_json_request(base_url: str, tags: str, limit: int = 1, page: int = 0) -> dict:
    params = {
        'limit': limit,
        'tags': tags,
        'page': page
    }

    resp = requests.get(f'{base_url}/posts.json', params)
    resp.raise_for_status()

    return resp.json()


def fetch_counts(base_url: str, tags: str) -> int:
    params = {
        'tags': tags
    }

    resp = requests.get(f'{base_url}/counts/posts.json', params)
    resp.raise_for_status()

    resp_json = resp.json()

    return resp_json.get('counts', {}).get('posts') or 0
