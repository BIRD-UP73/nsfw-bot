import logging
from typing import Dict

from posts.data.post_data import Post
from posts.fetcher.post_key_fetcher import PostKeyFetcher
from posts.post_entry_key import PostEntryKey
from posts.singleton import Singleton
from url.urls import UrlEnum


class PostEntryCache(metaclass=Singleton):
    entries: Dict[PostEntryKey, Post] = {}

    def add_post_data(self, post_data: Post, url: UrlEnum):
        entry_key = PostEntryKey(post_data.post_id, url)
        self.entries[entry_key] = post_data

    def get_post(self, post_key: PostEntryKey, skip_cache: bool = False) -> Post:
        if not skip_cache:
            cached_entry = self.entries.get(post_key)

            if cached_entry:
                logging.info(f'Fetching cached post, url={post_key.url}, id={post_key.post_id}')
                return cached_entry

        post_data = PostKeyFetcher.fetch(post_key)

        if post_key not in self.entries:
            logging.info(f'Adding post to cache, url={post_key.url}, id={post_key.post_id}')
            self.add_post_data(post_data, post_key.url)

        return post_data
