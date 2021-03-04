import random
from xml.dom.minidom import Element
from xml.etree import ElementTree

import requests

POST_LIMIT = 2500
MAX_POSTS_PER_PAGE = 100


def get_xml_post(tags: str, url: str) -> Element:
    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, 0, url)
    posts = ElementTree.fromstring(resp_text)

    total_posts = int(posts.get('count'))
    max_posts_to_search = min(total_posts, POST_LIMIT)
    max_pages = max_posts_to_search // MAX_POSTS_PER_PAGE

    if max_posts_to_search == 0:
        return 0, None

    random_page = random.randint(0, max_pages)

    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, random_page, url)
    posts = ElementTree.fromstring(resp_text)

    random.shuffle(posts)
    return total_posts, posts[0]


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


def send_request(limit: int, tags: str, page: int, url: str) -> str:
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
