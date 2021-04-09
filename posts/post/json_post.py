from discord.ext.commands import Context

from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.post.post_message import PostMessage
from util import util


async def show_post(ctx: Context, tags: str, score: int):
    if len(tags.split(' ')) < 2:
        tags = util.parse_tags(tags, score)

    fetcher = JsonPostFetcher(tags)
    await PostMessage(fetcher, ctx).create_message()
