import random
import xml.etree.ElementTree as et
from xml.dom.minidom import Element

import requests
from dateutil import parser
from discord import Embed, Color
from discord.ext.commands import Context

import util
from api.abstractpost import AbstractPost, AbstractPostData, PostError

POST_LIMIT = 2500
MAX_POSTS_PER_PAGE = 100


class XmlPostData(AbstractPostData):
    tags = ''

    def __init__(self, el: Element, total_posts):
        self.file_url = el.get('file_url')
        self.file_ext = self.file_url.split('.')[-1]
        self.created_at = el.get('created_at')
        self.score = el.get('score')
        self.source = el.get('source')
        self.tags = el.get('tags')
        self.total_posts = total_posts

    def to_content(self) -> dict:
        if not util.is_image(self.file_ext):
            return {'embed': None, 'content': self.file_url}

        embed = Embed()
        embed.colour = Color.green()

        if self.total_posts:
            embed.description = f'Found {self.total_posts} images'
        if self.created_at:
            embed.timestamp = parser.parse(self.created_at)
        if self.source:
            embed.add_field(name='Source', value=self.source, inline=False)
        if self.score:
            embed.set_footer(text=f'Score: {self.score}')
        if self.file_url:
            embed.set_image(url=self.file_url)

        return {'embed': embed, 'content': None}


class XmlPost(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        self.ctx = ctx
        self.url = url
        self.tags = tags

    def fetch_post(self):
        total_posts, xml_post = get_xml_post(self.tags, self.url)

        if total_posts == 0:
            return PostError(f'No images found for {self.tags}')

        post_data = XmlPostData(xml_post, total_posts)
        if post_data.has_disallowed_tags():
            return PostError('Post contains disallowed tags. Please try again.')

        self.update_hist(post_data)
        return post_data


def get_xml_post(tags: str, url: str) -> Element:
    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, 0, url)
    posts = et.fromstring(resp_text)

    total_posts = int(posts.get('count'))
    max_posts_to_search = min(total_posts, POST_LIMIT)
    max_pages = max_posts_to_search // MAX_POSTS_PER_PAGE

    if max_posts_to_search == 0:
        return 0, None

    random_page = random.randint(0, max_pages)

    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, random_page, url)
    posts = et.fromstring(resp_text)

    random.shuffle(posts)
    return total_posts, posts[0]


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    post = XmlPost(ctx, url, tags)
    await post.create_message()


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
