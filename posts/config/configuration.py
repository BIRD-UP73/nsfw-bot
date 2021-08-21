from typing import List

from discord.ext.commands import Context

from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.paginator import Paginator
from posts.post_message.post_message import PostMessage
from url.urls import UrlInfo

import re


class Configuration:
    url_info: UrlInfo
    max_posts = 200000

    async def create_post(self, ctx: Context, tags: str, score: int, emojis: List[str]):
        query = self.parse_tags(tags, score)
        count = self.fetch_count(query)

        paginator = self.paginator(count)

        fetcher = XmlPostFetcher(self.url_info, paginator)

        await PostMessage(fetcher, ctx, emojis).create_message()

    def paginator(self, post_count: int):
        return Paginator(post_count)

    def parse_tags(self, tags: str, score: int):
        if re.match('.*score:(>|>=|<|<=)\d*', tags):
            return tags

        return f'{tags} score:>={score}'

    def fetch_count(self, query: str):
        pass
