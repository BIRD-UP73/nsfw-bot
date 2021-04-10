from abc import abstractmethod, ABC
from typing import Union

from discord import DMChannel, TextChannel

from posts.data.post_data import Post


class AbstractPostFetcher(ABC):
    @abstractmethod
    def fetch_count(self) -> int:
        pass

    @abstractmethod
    def fetch_for_page(self, page: int, source: Union[DMChannel, TextChannel]):
        pass

    @abstractmethod
    def get_post(self) -> Post:
        pass
