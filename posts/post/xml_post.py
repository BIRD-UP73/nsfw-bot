import random
from xml.dom.minidom import Element
from xml.etree import ElementTree

from discord.ext.commands import Context, CommandError

from posts.api.xml_api import send_request
from posts.data.post_data import PostData
from posts.data.xml_post_data import XmlPostData
from posts.post.post import Post
from util import util


class XmlPost(Post):
    total_posts: int = 0

    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx, url, tags)

    async def create_message(self):
        self.total_posts = get_total_posts(self.url, self.tags)

        if self.total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

        await super().create_message()

    def fetch_post(self) -> PostData:
        random_page = random.randint(0, self.total_posts - 1)
        xml_post = fetch_xml_post(self.url, self.tags, random_page)

        return xml_post


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    post = XmlPost(ctx, url, tags)
    await post.create_message()


def get_total_posts(url: str, tags: str) -> int:
    # Fetch 0 posts to just get the post count
    resp_text = send_request(url, 0, tags, 0)
    posts = ElementTree.fromstring(resp_text)

    text_count = posts.get('count')

    if text_count:
        return int(text_count)

    return 0


def fetch_xml_post(url: str, tags: str, page: int) -> Element:
    resp_text = send_request(url, 1, tags, page)
    posts = ElementTree.fromstring(resp_text)

    if len(posts) == 0:
        return

    return XmlPostData.from_xml(posts[0])
