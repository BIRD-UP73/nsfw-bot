import random
from typing import Tuple
from xml.dom.minidom import Element
from xml.etree import ElementTree

from discord.ext.commands import Context, CommandError

from posts.api.xml_api import send_request
from posts.data.post_data import PostHasDisallowedTags
from posts.data.xml_post_data import XmlPostData
from posts.post.post import AbstractPost
from util import util


POST_LIMIT = 2500
MAX_POSTS_PER_PAGE = 100


class XmlPost(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx, url, tags)

    def fetch_post(self):
        total_posts, xml_post = get_xml_post(self.tags, self.url)

        if total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

        post_data = XmlPostData.from_xml(xml_post, total_posts)
        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    post = XmlPost(ctx, url, tags)
    await post.create_message()


def get_xml_post(tags: str, url: str) -> Tuple[int, Element]:
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
