import logging

from typing import Union

from discord import TextChannel, DMChannel
from discord.ext.commands import UserInputError

from posts.api.json_api import fetch_counts, send_json_request
from posts.data.json_post_data import JsonPost
from posts.data.post_data import ErrorPost
from posts.fetcher.post_fetcher import PostFetcher
from posts.post_history import PostHistory
from posts.paginator.json_post_paginator import JsonPostPaginator
from url.urls import URL
from util import tag_util


class JsonPostFetcher(PostFetcher):
    def __init__(self, url: URL, tags: str):
        super().__init__(url, tags)
        self.paginator = JsonPostPaginator()
        self.tags = tags

    def fetch_count(self) -> int:
        return min(1000, fetch_counts(self.url.long_url, self.tags))

    def fetch_for_page(self, page: int, source: Union[DMChannel, TextChannel]):
        resp_json = send_json_request(self.url.long_url, self.tags, page=page)

        if len(resp_json) == 0:
            logging.warning(f'JSON post not found, url={self.url}, tags={self.tags}, page={page}')
            self.post_data = ErrorPost('Could not find post.')
        else:
            self.post_data = JsonPost(self.url, **resp_json[0])

        PostHistory().add_to_history(source, self.post_data)
