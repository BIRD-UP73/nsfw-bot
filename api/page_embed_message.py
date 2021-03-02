from abc import ABC, abstractmethod
from typing import List

from discord import Reaction
from discord.ext.commands import Context

from api.post_entry import PostEntry
from db import post_repository


class PageEmbedMessage(ABC):
    message = None
    page = 0

    reaction_emojis = ['⬅', '➡', '🗑️', '⭐']

    def __init__(self, ctx: Context, data: List[PostEntry]):
        self.ctx: Context = ctx
        self.data: List[PostEntry] = data

    async def create_message(self):
        self.message = await self.ctx.send(**self.get_current_page())

        for reaction_emoji in self.reaction_emojis:
            await self.message.add_reaction(reaction_emoji)

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
            post_data = data.fetch_post()

            if not post_data.is_error() and not post_repository.exists(user, data.url, data.post_id):
                post_repository.store_favorite(user, data.url, data.post_id)
                await self.ctx.send(f'{user.mention}, successfully stored favorite.')

    async def after_reaction(self, reaction: Reaction, user):
        if self.ctx.guild:
            await self.message.remove_reaction(reaction.emoji, user)

    async def update_message(self):
        page_content = self.get_current_page()
        await self.message.edit(**page_content)

    def get_data(self) -> PostEntry:
        return self.data[self.page]

    @abstractmethod
    def get_current_page(self) -> dict:
        pass