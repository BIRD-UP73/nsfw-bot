from abc import ABC
from typing import Optional, Union

from discord import DMChannel, TextChannel

from posts.data.post_data import Post, NonExistentPost
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher
from posts.paginator.paginator import Paginator
from url.urls import UrlEnum


class PostFetcher(AbstractPostFetcher, ABC):
    def __init__(self, url: UrlEnum, tags: str, paginator: Paginator):
        super().__init__(paginator)
        self.url: UrlEnum = url
        self.tags: str = tags
        self.post_data: Optional[Post] = None

    def fetch_current_page(self, source: Union[DMChannel, TextChannel]):
        self.fetch_for_page(self.paginator.page, source)

    def get_post(self) -> Post:
        if self.post_data is None:
            return NonExistentPost()
        return self.post_data
