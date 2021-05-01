from abc import abstractmethod, ABC
from typing import Union

from discord import DMChannel, TextChannel

from posts.data.post_data import Post
from posts.paginator.paginator import Paginator


class AbstractPostFetcher(ABC):
    def __init__(self, paginator: Paginator):
        self.paginator: Paginator = paginator

    @abstractmethod
    def fetch_count(self):
        """
        Sets the post count in the paginator
        """
        pass

    @abstractmethod
    def fetch_current_page(self, source: Union[DMChannel, TextChannel]):
        pass

    @abstractmethod
    def fetch_for_page(self, page: int, source: Union[DMChannel, TextChannel]):
        pass

    @abstractmethod
    def get_post(self) -> Post:
        pass
