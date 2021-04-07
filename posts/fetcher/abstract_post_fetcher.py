from abc import abstractmethod, ABC
from typing import Union

from discord import DMChannel, TextChannel

from posts.data.post_data import PostData
from posts.paginator.paginator import Paginator, DefaultPaginator


class AbstractPostFetcher(ABC):
    def __init__(self, paginator: Paginator = DefaultPaginator()):
        self.paginator = paginator

    @abstractmethod
    def fetch_count(self):
        pass

    @abstractmethod
    def fetch_for_page(self, page: int, source: Union[DMChannel, TextChannel]):
        pass

    @abstractmethod
    def get_post(self) -> PostData:
        pass

    def next_page(self, source: Union[DMChannel, TextChannel]):
        page = self.paginator.next_page()
        return self.fetch_for_page(page, source)

    def previous_page(self, source: Union[DMChannel, TextChannel]):
        page = self.paginator.previous_page()
        return self.fetch_for_page(page, source)

    def random_page(self, source: Union[DMChannel, TextChannel]):
        page = self.paginator.random_page()
        return self.fetch_for_page(page, source)

    def current_page(self):
        return self.paginator.page
