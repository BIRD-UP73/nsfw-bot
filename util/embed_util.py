from abc import ABC, abstractmethod
from typing import List

from discord.ext.commands import Context

from api.api_db_wrapper import PostEntry
from db.post_repository import store_favorite


class PageEmbedMessage(ABC):
    message = None
    page = 0

    def __init__(self, ctx: Context, data: List[PostEntry]):
        self.ctx: Context = ctx
        self.data: List[PostEntry] = data

    async def create_message(self):
        self.message = await self.ctx.send(**self.get_current_page())

        await self.message.add_reaction('⬅')
        await self.message.add_reaction('➡')
        await self.message.add_reaction('🗑️')
        await self.message.add_reaction('⭐')

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
        if reaction.emoji == '⭐':
            data = self.get_data()
            store_favorite_result = store_favorite(user, data.url, data.post_id)
            if store_favorite_result:
                await self.ctx.send(f'{user.mention}, successfully stored favorite.')

    async def update_message(self):
        page_content = self.get_current_page()
        await self.message.edit(**page_content)

    def get_data(self) -> PostEntry:
        return self.data[self.page]

    @abstractmethod
    def get_current_page(self) -> dict:
        pass
