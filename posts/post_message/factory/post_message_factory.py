from discord.ext.commands import Context, UserInputError

from commands.nsfw.nsfw_command import CommandOptions
from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from posts.post_message.post_message import PostMessage
from url.urls import URL, Danbooru, Rule34Paheal, KonachanCom
from util import tag_util


def fetcher_for_url(url: URL, tags: str, score: int, max_posts: int):
    if url == Danbooru:
        return JsonPostFetcher(url, tags)

    return XmlPostFetcher(url, tags, score, max_posts)


def paginator_for_url(url: URL):
    if url == Danbooru or url == Rule34Paheal or url == KonachanCom:
        return JsonPostPaginator()


class PostMessageFactory:
    @staticmethod
    async def create_post(ctx: Context, options: CommandOptions, parsed_tags: str, score: int):
        parsed_tags = parsed_tags or ''

        split_tags = parsed_tags.split(' ')

        if options.url == Danbooru and len(split_tags) > 2:
            raise UserInputError(f'Maximum of 2 tags allowed. You entered {len(split_tags)}')

        parsed_tags = tag_util.parse_tags(parsed_tags, score)

        fetcher = fetcher_for_url(options.url, parsed_tags, score, options.max_posts)
        paginator = paginator_for_url(options.url)
        await PostMessage(fetcher, ctx, options.emojis, paginator).create_message()
