from typing import Optional

import requests
from dateutil import parser
from discord import Embed, Color
from discord.ext.commands import Context

import util
from api.abstractpost import AbstractPostData, PostError
from api.xml_api import AbstractPost

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPostData(AbstractPostData):
    artist_tag: str = ''
    character_tag: str = ''
    copyright_tag: str = ''
    created_at: str = ''
    file_ext: str = ''
    file_url: str = ''
    score: str = ''
    source: str = ''

    def __init__(self, json_dict: dict):
        self.artist_tag = json_dict.get('tag_string_artist')
        self.character_tag = json_dict.get('tag_string_character')
        self.copyright_tag = json_dict.get('tag_string_copyright')
        self.created_at = json_dict.get('created_at')
        self.file_ext = json_dict.get('file_ext')
        self.file_url = json_dict.get('file_url')
        self.score = json_dict.get('score')
        self.source = json_dict.get('source')
        self.tags = json_dict.get('tags')

    def to_content(self) -> dict:
        if not util.is_image(self.file_ext):
            return {'embed': None, 'content': self.file_url}

        embed = Embed()
        embed.colour = Color.green()

        if self.created_at:
            embed.timestamp = parser.parse(self.created_at)
        if self.copyright_tag and len(self.copyright_tag) < util.max_field_length:
            embed.add_field(name='Copyright', value=self.copyright_tag)
        if self.character_tag and len(self.character_tag) < util.max_field_length:
            embed.add_field(name='Characters', value=self.character_tag)
        if self.artist_tag and len(self.artist_tag) < util.max_field_length:
            embed.add_field(name='Artist', value=self.artist_tag)
        if self.source:
            embed.add_field(name='Source', value=self.source, inline=False)
        if self.score:
            embed.set_footer(text=f'Score: {self.score}')
        if self.file_url:
            embed.set_image(url=self.file_url)

        return {'embed': embed, 'content': None}


class JsonPost(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        self.ctx = ctx
        self.url = url
        self.tags = tags

    def fetch_post(self):
        json_post = get_json_post(self.tags)

        post_data = JsonPostData(json_post)

        if post_data.has_disallowed_tags():
            return PostError('Post contains disallowed tags. Please try again.')

        self.update_hist(post_data)
        return post_data


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
