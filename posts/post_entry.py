from datetime import datetime
from typing import Optional

from posts.data.post_data import Post
from url.urls import URL


class PostEntry:
    def __init__(self, url: URL, post_id: int, saved_at: datetime, post_data: Post = None):
        self.url: URL = url
        self.post_id: int = post_id
        self.saved_at: datetime = saved_at
        self.post_data: Optional[Post] = post_data

    def __eq__(self, other):
        return isinstance(other, PostEntry) and self.url == other.url and self.post_id == other.post_id

    @classmethod
    def from_post_data(cls, post: Post):
        return PostEntry(post.board_url, post.post_id, datetime.now())
