from datetime import datetime
from typing import Optional

from posts.data.post_data import Post
from util.url_util import parse_url


class PostEntry:
    def __init__(self, url: str, post_id: int, saved_at: datetime, post_data: Post = None):
        self.url: str = url
        self.post_id: int = post_id
        self.saved_at: datetime = saved_at
        self.post_data: Optional[Post] = post_data

    @classmethod
    def from_post_data(cls, post_data: Post):
        return PostEntry(parse_url(post_data.file_url), post_data.post_id, datetime.now())
