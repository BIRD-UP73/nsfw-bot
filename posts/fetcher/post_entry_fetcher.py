from datetime import datetime
from typing import List, Union

from discord import TextChannel, DMChannel

from posts.data.post_data import PostData
from posts.data.post_entry import PostEntry
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher
from posts.fetcher.post_entry_cache import PostEntryKey, PostEntryCache
from posts.history import PostHistory


class PostEntryFetcher(AbstractPostFetcher):
    def __init__(self, data: List[PostEntry]):
        super().__init__()
        self.data = data

    def fetch_for_page(self, page: int, source: Union[TextChannel, DMChannel]):
        entry = self.data[self.paginator.page]
        post_entry_key = PostEntryKey(entry.post_id, entry.url)

        post_data = PostEntryCache().get_post(post_entry_key)
        entry.post_data = post_data

        PostHistory().add_to_history(source, post_data)

    def fetch_count(self):
        self.paginator.post_count = len(self.data)

    def remove_post(self, page):
        del self.data[page]
        print(self.data)

    def current_post_timestamp(self) -> datetime:
        return self.data[self.paginator.page].saved_at

    def get_post(self) -> PostData:
        return self.data[self.paginator.page].post_data
