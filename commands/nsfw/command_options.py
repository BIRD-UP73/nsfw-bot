from typing import List

from url.urls import URL


class CommandOptions:
    def __init__(self, url: URL, emojis: List[str], max_posts: int = None):
        self.url = url
        self.emojis = emojis
        self.max_posts = max_posts
