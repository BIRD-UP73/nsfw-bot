import random


class Paginator:
    page: int = 0
    post_count: int = 0

    def random_page(self):
        if self.post_count > 0:
            self.page = random.randint(0, self.post_count - 1)

    def next_page(self):
        if self.post_count > 0:
            self.page = (self.page + 1) % self.post_count

    def previous_page(self):
        if self.post_count > 0:
            self.page = (self.page - 1) % self.post_count

    def display_page(self) -> int:
        return self.page + 1
