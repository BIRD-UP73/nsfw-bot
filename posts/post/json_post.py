from discord.ext.commands import Context

from posts.post.post_fetcher import JsonPostMessageFetcher
from posts.post.post_message import PostMessage
from util import util

danbooru_url = 'https://danbooru.donmai.us/posts.json'


async def show_post(ctx: Context, tags: str, score: int):
    if len(tags.split(' ')) < 2:
        tags = util.parse_tags(tags, score)

    post_message_fetcher = JsonPostMessageFetcher(danbooru_url, tags)
    post = PostMessage(ctx, post_message_fetcher)
    await post.create_message()
