from typing import Dict

from posts.data.post_data import Post
from posts.post_entry_key import PostEntryKey
from posts.fetcher.post_key_fetcher import PostKeyFetcher
from posts.singleton import Singleton


class PostEntryCache(metaclass=Singleton):
    entries: Dict[PostEntryKey, Post] = {}

    def add_post_data(self, post_data: Post, url: str):
        entry_key = PostEntryKey(post_data.post_id, url)
        self.entries[entry_key] = post_data

    def get_post(self, post_key: PostEntryKey, skip_cache: bool = False) -> Post:
        if not skip_cache:
            cached_entry = self.entries.get(post_key)

            if cached_entry:
                return cached_entry

        post_data = PostKeyFetcher.fetch(post_key)

        if post_key not in self.entries:
            self.add_post_data(post_data, post_key.url)

        return post_data
