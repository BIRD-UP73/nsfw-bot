from typing import List, Union, Deque, Optional

from discord import Member, User, Reaction
from discord.ext.commands import Context

from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class PageEmbedMessage(AbstractPost):
    emojis = ['🗑️', '⬅', '➡', '⭐']

    def __init__(self, ctx: Context, data: Union[List[PostEntry], Deque[PostEntry]]):
        super().__init__(ctx)
        self.data: Union[List[PostEntry], Deque[PostEntry]] = data
        self.page = 0
        self.message = None

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> Optional[bool]:
        result = await super().handle_reaction(reaction, user)

        if result is not None:
            return result

        if reaction.emoji == '➡':
            await self.next_page()
            return True
        if reaction.emoji == '⬅':
            await self.previous_page()
            return True

    async def next_page(self):
        self.page = (self.page + 1) % len(self.data)
        await self.update_message()

    async def previous_page(self):
        self.page = (self.page - 1) % len(self.data)
        await self.update_message()

    async def update_message(self):
        page_content = self.page_content()
        await self.message.edit(**page_content.to_dict())

    def to_post_entry(self) -> PostEntry:
        return self.data[self.page]

    def page_content(self) -> PostMessageContent:
        return self.to_post_entry().post_data.to_message_content()
