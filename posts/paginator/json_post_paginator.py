import random

from posts.paginator.paginator import Paginator


class JsonPostPaginator(Paginator):
    def random_page(self):
        self.page = random.randint(1, self.post_count)

    def next_page(self):
        if self.page == self.post_count:
            self.page = 1
        else:
            self.page += 1

    def previous_page(self):
        if self.page == 1:
            self.page = self.post_count
        else:
            self.page -= 1

    def display_page(self) -> int:
        return self.page
