from typing import List, Union

from discord import TextChannel, DMChannel

from posts.data.post_data import PostData
from posts.data.post_entry import PostEntry
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher
from posts.fetcher.post_entry_cache import PostEntryKey, PostEntryCache
from posts.history import PostHistory
from posts.paginator.paginator import Paginator


class PostEntryFetcher(AbstractPostFetcher):
    def __init__(self, data: List[PostEntry], paginator: Paginator):
        super().__init__()
        self.data = data
        self.paginator = paginator

    def fetch_for_page(self, page: int, source: Union[TextChannel, DMChannel]):
        entry = self.data[page]
        post_entry_key = PostEntryKey(entry.post_id, entry.url)

        post_data = PostEntryCache().get_post(post_entry_key)
        entry.post_data = post_data

        PostHistory().add_to_history(source, post_data)

    def get_post(self) -> PostData:
        return self.data[self.paginator.page].post_data

    def fetch_count(self) -> int:
        return len(self.data)

    def remove_post(self, page):
        del self.data[page]

        if self.paginator.page == len(self.data):
            self.paginator.page = 0

        self.paginator.post_count -= 1

    def current_entry(self) -> PostEntry:
        return self.data[self.paginator.page]
