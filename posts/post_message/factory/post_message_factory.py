from discord.ext.commands import Context, UserInputError

from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from posts.post_message.post_message import PostMessage
from url.urls import URL
from util import tag_util


class PostMessageFactory:

    @staticmethod
    async def create_post(ctx: Context, url: URL, tags: str, score: int, max_count: int = None):
        if url == URL.DANBOORU:
            await PostMessageFactory.create_json_post(ctx, url, tags, score)
        else:
            await PostMessageFactory.create_xml_post(ctx, url, tags, score, max_count)

    @staticmethod
    async def create_json_post(ctx: Context, url: URL, tags: str, score: int):
        split_tags = tags.split(' ')

        if len(split_tags) > 2:
            raise UserInputError(f'Maximum of 2 tags allowed. You entered {len(split_tags)}')
        elif len(split_tags) < 2:
            tags = tag_util.parse_tags(tags, score)

        fetcher = JsonPostFetcher(url.long_url, tags)
        await PostMessage(fetcher, ctx, JsonPostPaginator()).create_message()

    @staticmethod
    async def create_xml_post(ctx: Context, url: URL, tags: str, score: int, max_count: int = None):
        tags = tag_util.parse_tags(tags, score)

        fetcher = XmlPostFetcher(url.long_url, tags, max_count)
        await PostMessage(fetcher, ctx).create_message()
