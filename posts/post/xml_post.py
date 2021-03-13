import random
from xml.etree import ElementTree

from discord.ext.commands import Context, CommandError

from posts.api.xml_api import send_request
from posts.data.post_data import PostData, PostNoLongerExists
from posts.data.xml_post_data import XmlPostData
from posts.post.post_fetcher import PostMessageFetcher
from posts.post.post_message import PostMessage
from util import util


class XmlPostMessageFetcher(PostMessageFetcher):
    post_page: int = 0
    total_posts = 0

    def fetch_total_pages(self):
        self.total_posts = get_total_posts(self.url, self.tags)

        if self.total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

    def fetch_post(self) -> PostData:
        self.post_page = random.randint(0, self.total_posts - 1)
        self.post_data = fetch_xml_post(self.url, self.tags, self.post_page)
        return self.post_data


class XmlPostMessage(PostMessage):
    fetcher: XmlPostMessageFetcher

    async def create_message(self):
        self.fetcher.fetch_total_pages()
        self.get_post()
        await super().create_message()

    def post_content(self) -> dict:
        post_data = self.fetcher.post_data

        if post_data.is_animated():
            return dict(content=post_data.to_text(), embed=None)

        embed = post_data.to_embed()
        embed.description = f'Post **{self.fetcher.post_page}** of **{self.fetcher.total_posts}**'

        return dict(content=None, embed=embed)


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    fetcher = XmlPostMessageFetcher(url, tags)
    post = XmlPostMessage(ctx, fetcher)
    await post.create_message()


def get_total_posts(url: str, tags: str) -> int:
    # Fetch 0 posts to just get the post count
    resp_text = send_request(url, 0, tags, 0)
    posts = ElementTree.fromstring(resp_text)

    text_count = posts.get('count')

    if text_count:
        return int(text_count)

    return 0


def fetch_xml_post(url: str, tags: str, page: int) -> PostData:
    resp_text = send_request(url, 1, tags, page)
    posts = ElementTree.fromstring(resp_text)

    if len(posts) == 0:
        return PostNoLongerExists()

    return XmlPostData.from_xml(posts[0])
