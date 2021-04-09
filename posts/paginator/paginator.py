import random
from abc import ABC, abstractmethod


class Paginator(ABC):
    def __init__(self):
        self.post_count: int = 0
        self.page: int = 0

    @abstractmethod
    def next_page(self):
        pass

    @abstractmethod
    def previous_page(self):
        pass

    @abstractmethod
    def random_page(self):
        pass


class DefaultPaginator(Paginator):
    def random_page(self) -> int:
        self.page = random.randint(0, self.post_count - 1)
        return self.page

    def next_page(self) -> int:
        self.page = (self.page + 1) % self.post_count
        return self.page

    def previous_page(self) -> int:
        self.page = (self.page - 1) % self.post_count
        return self.page
