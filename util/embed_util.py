from abc import ABC, abstractmethod
from typing import List

from discord.ext.commands import Context


class PageData(ABC):

    @abstractmethod
    def to_content(self) -> dict:
        pass


class PageEmbedMessage(ABC):
    message = None
    page = 0

    def __init__(self, ctx: Context, data: List[PageData]):
        self.ctx = ctx
        self.data = data

    async def create_message(self):
        self.message = await self.ctx.send(**self.get_data().to_content())

        await self.message.add_reaction('⬅')
        await self.message.add_reaction('➡')
        await self.message.add_reaction('🗑️')

        self.ctx.bot.add_listener(self.on_reaction_add)

    async def on_reaction_add(self, reaction, user):
        if user == self.ctx.bot.user or self.message.id != reaction.message.id:
            return

        if reaction.emoji == '➡':
            self.page = (self.page + 1) % len(self.data)
            await self.update_message()
        if reaction.emoji == '⬅':
            self.page = (self.page - 1) % len(self.data)
            await self.update_message()

    async def update_message(self):
        page = self.get_current_page()
        await self.message.edit(**page)

    def get_data(self):
        return self.data[self.page]

    @abstractmethod
    def get_current_page(self) -> dict:
        pass
