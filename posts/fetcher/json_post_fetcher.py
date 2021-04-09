from typing import Union

from discord import TextChannel, DMChannel

from posts.api.json_api import fetch_counts, send_json_request
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import ErrorPost
from posts.fetcher.post_fetcher import PostFetcher
from posts.history import PostHistory
from posts.paginator.json_post_paginator import JsonPostPaginator

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPostFetcher(PostFetcher):
    def __init__(self, tags: str):
        super().__init__(danbooru_url, tags)
        self.paginator = JsonPostPaginator()

    def fetch_count(self) -> int:
        return min(1000, fetch_counts(self.tags))

    def fetch_for_page(self, page: int, source: Union[DMChannel, TextChannel]):
        resp_json = send_json_request(danbooru_url, self.tags, page=page)

        if len(resp_json) == 0:
            self.post_data = ErrorPost('Could not find post.')
        else:
            self.post_data = JsonPostData(**resp_json[0])

        PostHistory().add_to_history(source, self.post_data)
