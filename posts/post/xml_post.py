import random
from xml.dom.minidom import Element
from xml.etree import ElementTree

from discord.ext.commands import Context, CommandError

from posts.api.xml_api import send_request
from posts.data.post_data import PostHasDisallowedTags, PostData
from posts.data.xml_post_data import XmlPostData
from posts.post.post import AbstractPost
from util import util


class XmlPost(AbstractPost):
    total_posts: int = 0

    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx, url, tags)

    async def create_message(self):
        self.total_posts = get_total_posts(self.url, self.tags)

        if self.total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

        await super().create_message()

    def fetch_post(self) -> PostData:
        xml_post = random_xml_post(self.url, self.tags, self.total_posts)

        post_data = XmlPostData.from_xml(xml_post, self.total_posts)
        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    post = XmlPost(ctx, url, tags)
    await post.create_message()


def get_total_posts(url: str, tags: str) -> int:
    """
    Returns the total amount of posts for a list of tags

    :param url: the url to search the pots for
    :param tags: the tags
    :return: the total amount of posts for a tag
    """
    resp_text = send_request(url, 0, tags, 0)
    posts = ElementTree.fromstring(resp_text)

    text_count = posts.get('count')

    if text_count:
        return int(text_count)

    return 0


def random_xml_post(url: str, tags: str, total_posts: int) -> Element:
    random_page = random.randint(0, total_posts - 1)

    resp_text = send_request(url, 1, tags, random_page)
    posts = ElementTree.fromstring(resp_text)

    return posts[0]
