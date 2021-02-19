from abc import ABC, abstractmethod

from discord import Reaction, User, Message, Emoji
from discord.ext.commands import Context

import db.repo
from api.post_data import AbstractPostData


class AbstractPost(ABC):
    ctx: Context = None
    msg: Message = None
    post_data: AbstractPostData = None
    url: str = None
    tags: str = None

    async def create_message(self):
        self.fetch_post()
        self.msg = await self.ctx.send(**self.post_data.to_content())

        self.ctx.bot.add_listener(self.on_reaction_add)
        await self.msg.add_reaction('🗑️')
        await self.msg.add_reaction('🔁')
        await self.msg.add_reaction('⭐')

    def update_hist(self, post_data):
        """
        Adds the current post to the post history
        """
        hist_cog = self.ctx.bot.get_cog('PostHist')
        hist_cog.add_post(self.ctx.channel, post_data.file_url)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        if reaction.message.id != self.msg.id or user == self.ctx.bot.user:
            return
        if user == self.ctx.author:
            await self.handle_reaction(user, reaction.emoji)
        if self.ctx.guild:
            await self.msg.remove_reaction(reaction.emoji, user)

    async def handle_reaction(self, user: User, emoji: Emoji):
        if emoji == '🗑️':
            await self.msg.delete()
            self.ctx.bot.remove_listener(self.on_reaction_add)
            return
        if emoji == '🔁':
            self.fetch_post()
            await self.msg.edit(**self.post_data.to_content())
        if emoji == '⭐':
            if db.repo.store_favorite(user, self.post_data):
                await self.ctx.send(f'{self.ctx.author.mention}, added post to favorites')

    @abstractmethod
    def fetch_post(self):
        """
        Abstract method to fetch a post, should return `AbstractPostData`
        Method should set `self.post_data`
        """
        pass
