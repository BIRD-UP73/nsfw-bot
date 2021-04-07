import random

from posts.paginator.paginator import DefaultPaginator


class JsonPostPaginator(DefaultPaginator):
    def __init__(self):
        super().__init__()
        self.page = 1

    def random_page(self) -> int:
        self.page = random.randint(1, self.post_count)
        return self.page

    def next_page(self):
        if self.page == self.post_count:
            self.page = 1
        else:
            self.page += 1

        return self.page

    def previous_page(self) -> int:
        if self.page == 1:
            self.page = self.post_count
        else:
            self.page -= 1

        return self.page
