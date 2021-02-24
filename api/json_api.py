from typing import Optional

import requests
from discord import Embed
from discord.ext.commands import Context, CommandError

from api.post import AbstractPost
from api.post_data import PostError, PostData
from util import util

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPostData(PostData):
    artist_tag: str = ''
    character_tag: str = ''
    copyright_tag: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artist_tag = kwargs.get('tag_string_artist')
        self.character_tag = kwargs.get('tag_string_character')
        self.copyright_tag = kwargs.get('tag_string_copyright')

    def to_embed(self) -> Embed:
        embed = super().to_embed()

        if self.copyright_tag and len(self.copyright_tag) < util.max_field_length:
            embed.add_field(name='Copyright', value=self.copyright_tag)
        if self.character_tag and len(self.character_tag) < util.max_field_length:
            embed.add_field(name='Characters', value=self.character_tag)
        if self.artist_tag and len(self.artist_tag) < util.max_field_length:
            embed.add_field(name='Artist', value=self.artist_tag)

        return embed


class JsonPost(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        self.ctx = ctx
        self.url = url
        self.tags = tags

    def fetch_post(self) -> PostData:
        """
        Fetches a post from a site with a json-based API
        Will throw an error if no posts are found (nothing else to fetch)
        Will show an error embed if the post contains disallowed tags

        Also adds post to history

        :return: the fetched post
        """
        json_post = get_json_post(self.tags)

        if not json_post:
            raise CommandError(f'No posts found for {self.tags}')

        post_data = JsonPostData(**json_post)

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


def json_post_by_id(base_url: str, post_id: int):
    url = f'{base_url}/{post_id}.json'
    resp = requests.get(url)

    resp.raise_for_status()

    return resp.json()


def send_json_request(url: str, tags: str, random: bool = True):
    params = {
        'limit': '1',
        'random': random,
        'tags': tags
    }

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.json()
