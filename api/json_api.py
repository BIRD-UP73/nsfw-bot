from typing import Optional

import requests
from discord.ext.commands import Context

import util
from api.post import PostData
from api.xml_api import Post

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPost(Post):
    def fetch_post(self):
        json_post = get_json_post(self.tags)

        while 'loli' in json_post.get('tag_string'):
            json_post = get_json_post(self.tags)

        self.post_data = PostData.from_json(json_post)
        self.update_hist()


async def show_post(ctx: Context, tags: str, score: int):
    if len(tags.split(' ')) < 2:
        tags = util.parse_tags(tags, score)

    post = JsonPost(ctx, danbooru_url, tags)
    await post.create_message()


def get_json_post(tags: str) -> Optional[dict]:
    resp_json = send_json_request(danbooru_url, tags)

    if len(resp_json) == 0:
        return None

    return resp_json[0]


def send_json_request(url: str, tags: str, random: bool = True):
    params = {
        'limit': '1',
        'random': random,
        'tags': tags
    }

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.json()
