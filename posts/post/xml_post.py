import random
from xml.dom.minidom import Element
from xml.etree import ElementTree

from discord.ext.commands import Context, CommandError

from posts.api.xml_api import send_request
from posts.data.post_data import PostData, NonExistentPost
from posts.data.xml_post_data import XmlPostData
from posts.message.post_message_content import PostMessageContent
from posts.post.post_message import PostMessage
from util import util


class XmlPostMessage(PostMessage):
    total_posts: int = 0

    async def create_message(self):
        self.total_posts = get_total_posts(self.url, self.tags)

        if self.total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

        await super().create_message()

    def fetch_random_post(self):
        self.page = random.randint(0, self.total_posts - 1)
        self.post_data = fetch_xml_post(self.url, self.tags, self.page)

    async def next_page(self):
        self.page = (self.page + 1) % self.total_posts
        self.post_data = fetch_xml_post(self.url, self.tags, self.page)
        await self.update_message()

    async def previous_page(self):
        self.page = (self.page - 1) % self.total_posts
        self.post_data = fetch_xml_post(self.url, self.tags, self.page)
        await self.update_message()

    def page_content(self) -> PostMessageContent:
        message_content = super().page_content()

        if message_content.embed:
            message_content.embed.description = f'Post **{self.page}** of **{self.total_posts}**'

        return message_content


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    await XmlPostMessage(ctx, url, tags).create_message()


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
        return NonExistentPost()

    return XmlPostData.from_xml(posts[0])
