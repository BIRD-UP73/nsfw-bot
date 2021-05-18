from typing import List, Union

from discord import TextChannel, DMChannel

from posts.data.post_data import Post
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher
from posts.fetcher.post_entry_cache import PostEntryKey, PostEntryCache
from posts.paginator.paginator import Paginator
from posts.post_entry import PostEntry
from posts.post_history import PostHistory


class PostEntryFetcher(AbstractPostFetcher):
    def __init__(self, data: List[PostEntry], paginator: Paginator):
        super().__init__(paginator)
        self.data: List[PostEntry] = data

    def fetch_current_page(self, source: Union[DMChannel, TextChannel]):
        self.fetch_for_page(self.paginator.page, source)

    def fetch_for_page(self, page: int, source: Union[TextChannel, DMChannel]):
        entry = self.data[page]
        post_entry_key = PostEntryKey(entry.post_id, entry.url)

        post_data = PostEntryCache().get_post(post_entry_key)
        entry.post_data = post_data

        PostHistory().add_to_history(source, post_data)

    def get_post(self) -> Post:
        return self.data[self.paginator.page].post_data

    def fetch_count(self):
        self.paginator.post_count = len(self.data)

    def remove_post(self, post_entry: PostEntry):
        if post_entry in self.data:
            post_index = self.data.index(post_entry)
            self.remove_post_for_page(post_index)

    def remove_post_for_page(self, page):
        del self.data[page]

        if self.paginator.page == self.paginator.post_count - 1:
            self.paginator.page = 0

        if self.paginator.page > page:
            self.paginator.page -= 1

        self.paginator.post_count -= 1

    def current_entry(self) -> PostEntry:
        return self.data[self.paginator.page]
