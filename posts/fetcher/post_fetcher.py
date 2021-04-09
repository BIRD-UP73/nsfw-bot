from abc import ABC
from typing import Optional

from posts.data.post_data import PostData, DisallowedTagsPost, NonExistentPost
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher


class PostFetcher(AbstractPostFetcher, ABC):
    def __init__(self, url: str, tags: str):
        super().__init__()
        self.url = url
        self.tags = tags
        self.post_data: Optional[PostData] = None

    def get_post(self) -> PostData:
        if self.post_data is None:
            return NonExistentPost()
        return self.post_data
