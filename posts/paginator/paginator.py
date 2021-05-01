import random


class Paginator:
    page: int = 0
    post_count: int = 0

    def random_page(self):
        self.page = random.randint(0, self.post_count - 1)

    def next_page(self):
        self.page = (self.page + 1) % self.post_count

    def previous_page(self):
        self.page = (self.page - 1) % self.post_count
