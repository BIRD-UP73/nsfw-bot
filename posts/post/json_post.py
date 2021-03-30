from discord.ext.commands import Context, CommandError

from posts.api.json_api import send_json_request
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import PostData
from posts.post.post_message import PostMessage
from util import util

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPostMessage(PostMessage):
    max_pages = 1000

    def fetch_random_post(self):
        resp_json = send_json_request(danbooru_url, self.tags)

        if len(resp_json) == 0:
            raise CommandError(f'No posts found for {self.tags}')

        self.post_data = JsonPostData(**resp_json[0])

    async def next_page(self):
        self.page = (self.page + 1) % self.max_pages
        self.page = 555
        resp_json = send_json_request(danbooru_url, self.tags, random=False, page=self.page)

        if len(resp_json) == 0:
            return await self.channel.send('Reached end')

        self.post_data = JsonPostData(**resp_json)
        await self.update_message()

    async def previous_page(self):
        self.page = (self.page - 1) % self.max_pages
        resp_json = send_json_request(danbooru_url, self.tags, random=False, page=self.page)

        if len(resp_json) == 0:
            return await self.channel.send('Reached end')

        self.post_data = JsonPostData(**resp_json)
        await self.update_message()


async def show_post(ctx: Context, tags: str, score: int):
    if len(tags.split(' ')) < 2:
        tags = util.parse_tags(tags, score)

    await JsonPostMessage(ctx, danbooru_url, tags).create_message()
