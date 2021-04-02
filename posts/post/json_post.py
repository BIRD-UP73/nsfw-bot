import random

from discord.ext.commands import Context

from posts.api.json_api import send_json_request, fetch_counts
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import ErrorPost
from posts.post.post_message import PostMessage
from util import util

danbooru_url = 'https://danbooru.donmai.us/posts.json'
max_pages = 1000


class JsonPostMessage(PostMessage):
    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx, url, tags)
        self.page = 1

    def fetch_total_posts(self):
        self.total_posts = min(1000, fetch_counts(self.tags))

    def fetch_random_post(self):
        self.page = random.randint(1, self.total_posts)
        self.fetch_post_for_page()

    async def next_page(self):
        if self.page == self.total_posts:
            self.page = 1
        else:
            self.page += 1

        self.fetch_post_for_page()
        await self.update_message()

    async def previous_page(self):
        if self.page == 1:
            self.page = self.total_posts
        else:
            self.page -= 1

        self.fetch_post_for_page()
        await self.update_message()

    def fetch_post_for_page(self):
        resp_json = send_json_request(danbooru_url, self.tags, page=self.page)

        if len(resp_json) == 0:
            self.post_data = ErrorPost('Could not find post.')
        else:
            self.post_data = JsonPostData(**resp_json[0])


async def show_post(ctx: Context, tags: str, score: int):
    if len(tags.split(' ')) < 2:
        tags = util.parse_tags(tags, score)

    await JsonPostMessage(ctx, danbooru_url, tags).create_message()
