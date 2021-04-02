from typing import List, Union, Deque

from discord.ext.commands import Context

from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class PageEmbedMessage(AbstractPost):
    def __init__(self, ctx: Context, data: Union[List[PostEntry], Deque[PostEntry]]):
        super().__init__(ctx)
        self.data: Union[List[PostEntry], Deque[PostEntry]] = data
        self.page = 0

    async def next_page(self):
        self.page = (self.page + 1) % len(self.data)
        await self.update_message()

    async def previous_page(self):
        self.page = (self.page - 1) % len(self.data)
        await self.update_message()

    def to_post_entry(self) -> PostEntry:
        return self.data[self.page]

    def page_content(self) -> PostMessageContent:
        return self.to_post_entry().post_data.to_message_content()
