from abc import ABC
from typing import Optional

from posts.data.post_data import Post, NonExistentPost
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher


class PostFetcher(AbstractPostFetcher, ABC):
    def __init__(self, url: str, tags: str):
        self.url = url
        self.tags = tags
        self.post_data: Optional[Post] = None

    def get_post(self) -> Post:
        if self.post_data is None:
            return NonExistentPost()
        return self.post_data
