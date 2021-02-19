import random
from xml.dom.minidom import Element
from xml.etree import ElementTree

import requests
from discord import Embed
from discord.ext.commands import Context

import util
from api.post import AbstractPost
from api.post_data import PostData, PostError

POST_LIMIT = 2500
MAX_POSTS_PER_PAGE = 100


class XmlPostData(PostData):
    total_posts = 0

    def __init__(self, total_posts, **kwargs):
        super().__init__(**kwargs)
        self.total_posts = total_posts

    @classmethod
    def from_xml(cls, el: ElementTree, total_posts: int):
        file_url = el.get('file_url')

        data = dict(
            file_url=file_url,
            file_ext=file_url.split('.')[-1],
            created_at=el.get('created_at'),
            score=el.get('score'),
            source=el.get('source'),
            tags=el.get('tags')
        )

        return cls(total_posts, **data)

    def to_embed(self) -> Embed:
        embed = super().to_embed()
        embed.description = f'Found {self.total_posts} images'
        return embed


class XmlPost(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        self.ctx = ctx
        self.url = url
        self.tags = tags

    def fetch_post(self):
        total_posts, xml_post = get_xml_post(self.tags, self.url)

        if total_posts == 0:
            return PostError(f'No images found for {self.tags}')

        post_data = XmlPostData.from_xml(xml_post, total_posts)
        if post_data.has_disallowed_tags():
            return PostError('Post contains disallowed tags. Please try again.')

        self.update_hist(post_data)
        self.post_data = post_data


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
