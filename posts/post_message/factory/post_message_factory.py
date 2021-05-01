from discord.ext.commands import Context

from commands.nsfw.nsfw_command import CommandOptions
from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.fetcher.post_fetcher import PostFetcher
from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from posts.paginator.paginator import Paginator
from posts.post_message.post_message import PostMessage
from url.urls import URL, Danbooru, Rule34Paheal, KonachanCom


def paginator_for_url(url: URL) -> Paginator:
    if url == Danbooru or url == Rule34Paheal or url == KonachanCom:
        return JsonPostPaginator()

    return Paginator()


def fetcher_for_url(url: URL, tags: str, score: int, max_posts: int) -> PostFetcher:
    paginator = paginator_for_url(url)

    if url == Danbooru:
        return JsonPostFetcher(url, tags, paginator)

    return XmlPostFetcher(url, tags, score, paginator, max_posts)


class PostMessageFactory:
    @staticmethod
    async def create_post(ctx: Context, options: CommandOptions, parsed_tags: str, score: int):
        fetcher = fetcher_for_url(options.url, parsed_tags, score, options.max_posts)
        await PostMessage(fetcher, ctx, options.emojis).create_message()
