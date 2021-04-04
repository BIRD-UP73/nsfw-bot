from typing import List, Union, Deque

from discord.ext.commands import Context

from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class PageEmbedMessage(AbstractPost):
    def __init__(self, ctx: Context, data: Union[List[PostEntry], Deque[PostEntry]]):
        super().__init__(ctx)
        self.data: Union[List[PostEntry], Deque[PostEntry]] = data

    def fetch_post_for_page(self):
        return None

    def fetch_total_posts(self):
        self.total_posts = len(self.data)

    def to_post_entry(self) -> PostEntry:
        return self.data[self.page]

    def page_content(self) -> PostMessageContent:
        return self.to_post_entry().post_data.to_message_content()
