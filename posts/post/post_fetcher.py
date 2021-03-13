from abc import ABC, abstractmethod
from typing import List

from discord.ext.commands import CommandError

from posts.api.json_api import send_json_request
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import PostData
from posts.data.post_entry import PostEntry


class PostFetcher(ABC):
    @abstractmethod
    def fetch_post(self):
        pass

    def get_post(self):
        return


class PostMessageFetcher(PostFetcher, ABC):
    post_data: PostData = None

    def __init__(self, url: str, tags: str):
        self.url: str = url
        self.tags: str = tags


class JsonPostMessageFetcher(PostMessageFetcher):
    def fetch_post(self) -> PostData:
        if self.post_data:
            return self.post_data

        resp_json = send_json_request(self.url, self.tags)

        if len(resp_json) == 0:
            raise CommandError(f'No posts found for {self.tags}')

        return JsonPostData(**resp_json[0])


class PostEntryFetcher(PostFetcher):
    page: int = 0

    def __init__(self, entries: List[PostEntry]):
        super().__init__()
        self.entries = entries

    def set_page(self, page: int):
        self.page = page

    def current_entry(self) -> PostEntry:
        return self.entries[self.page]

    def remove_current_post(self):
        self.entries.remove(self.current_entry())

    @property
    def post_data(self):
        return self.fetch_post()

    @property
    def url(self):
        return self.current_entry().url

    def fetch_post(self) -> PostData:
        entry = self.current_entry()
        if entry.post_data:
            return entry.post_data

        return entry.fetch_post()
