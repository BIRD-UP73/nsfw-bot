from discord.ext.commands import Context, UserInputError

from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from posts.post.post_message import PostMessage
from util import util
from util.url_util import get_long_url


class PostFactory:

    @staticmethod
    async def create_json_post(ctx: Context, tags: str, score: int):
        long_url = get_long_url(ctx.command.name)

        split_tags = tags.split(' ')

        if len(split_tags) < 2:
            tags = util.parse_tags(tags, score)
        else:
            raise UserInputError('Too many tags entered')

        fetcher = JsonPostFetcher(tags)
        await PostMessage(fetcher, ctx, JsonPostPaginator()).create_message()

    @staticmethod
    async def create_xml_post(ctx: Context, tags: str, score: int):
        long_url = get_long_url(ctx.command.name)
        tags = util.parse_tags(tags, score)

        fetcher = XmlPostFetcher(long_url, tags)
        await PostMessage(fetcher, ctx).create_message()

    @staticmethod
    async def create_tbib_post(ctx: Context, tags: str):
        """
        Tbib does not use score
        """
        long_url = get_long_url(ctx.command.name)

        fetcher = XmlPostFetcher(long_url, tags)
        await PostMessage(fetcher, ctx).create_message()
