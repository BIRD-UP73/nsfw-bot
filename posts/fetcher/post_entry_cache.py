from typing import Dict

from posts.data.post_data import PostData
from posts.fetcher.post_entry_key import PostEntryKey
from posts.fetcher.post_key_fetcher import PostKeyFetcher
from posts.singleton import Singleton


class PostEntryCache(metaclass=Singleton):
    entries: Dict[PostEntryKey, PostData] = {}

    def add_post_data(self, post_data: PostData, url: str):
        entry_key = PostEntryKey(post_data.post_id, url)
        self.entries[entry_key] = post_data

    def get_post(self, post_key: PostEntryKey, skip_cache: bool = False) -> PostData:
        if not skip_cache:
            cached_entry = self.entries.get(post_key)

            if cached_entry:
                return cached_entry

        post_data = PostKeyFetcher.fetch(post_key)

        if post_key not in self.entries:
            self.add_post_data(post_data, post_key.url)

        return post_data
