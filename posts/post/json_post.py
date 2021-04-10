from discord.ext.commands import Context

from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from posts.post.post_message import PostMessage
from util import tag_util


async def show_post(ctx: Context, tags: str, score: int, url: str):
    if len(tags.split(' ')) < 2:
        tags = tag_util.parse_tags(tags, score)

    fetcher = JsonPostFetcher(url, tags)
    await PostMessage(fetcher, ctx, JsonPostPaginator()).create_message()
