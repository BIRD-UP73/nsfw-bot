from discord.ext.commands import Context, UserInputError

from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from posts.post.post_message import PostMessage
from util import tag_util
from util.url_util import get_long_url


class PostFactory:

    @staticmethod
    async def create_json_post(ctx: Context, tags: str, score: int):
        long_url = get_long_url(ctx.command.name)
        split_tags = tags.split(' ')

        if len(split_tags) > 2:
            raise UserInputError(f'Maximum of 2 tags allowed. You entered {len(split_tags)}')
        elif len(split_tags) < 2:
            tags = tag_util.parse_tags(tags, score)

        fetcher = JsonPostFetcher(tags, long_url)
        await PostMessage(fetcher, ctx, JsonPostPaginator()).create_message()

    @staticmethod
    async def create_xml_post(ctx: Context, tags: str, score: int):
        long_url = get_long_url(ctx.command.name)
        tags = tag_util.parse_tags(tags, score)

        fetcher = XmlPostFetcher(long_url, tags)
        await PostMessage(fetcher, ctx).create_message()
