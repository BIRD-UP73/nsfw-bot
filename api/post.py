from abc import ABC, abstractmethod

from discord import Reaction, User, Message
from discord.ext.commands import Context

import db.post_repository
from api.post_data import PostData, PostError


class AbstractPost(ABC):
    ctx: Context = None
    message: Message = None
    post_data: PostData = None
    url: str = None
    tags: str = None

    async def create_message(self):
        """
        Creates a message with the post, and adds reaction listeners
        """
        self.fetch_post()
        self.message = await self.ctx.send(**self.post_data.to_content())

        self.ctx.bot.add_listener(self.on_reaction_add)
        await self.message.add_reaction('🗑️')
        await self.message.add_reaction('🔁')
        await self.message.add_reaction('⭐')

    def update_hist(self, post_data):
        """
        Adds the current post to the post history
        """
        hist_cog = self.ctx.bot.get_cog('PostHist')
        hist_cog.add_post(self.ctx.channel, post_data.file_url)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        """
        Function to handle user reactions to posts
        :param reaction: the reaction
        :param user: the user that reacted
        """
        if reaction.message.id != self.message.id or user == self.ctx.bot.user:
            return
        if reaction.emoji == '⭐' and not isinstance(self.post_data, PostError):
            if db.post_repository.store_favorite(user, self.post_data):
                await self.ctx.send(f'{self.ctx.author.mention}, added post to favorites')
        if user == self.ctx.author:
            if reaction.emoji == '🗑️':
                await self.message.delete()
                self.ctx.bot.remove_listener(self.on_reaction_add)
                return
            if reaction.emoji == '🔁':
                self.fetch_post()
                await self.message.edit(**self.post_data.to_content())
        if self.ctx.guild:
            await self.message.remove_reaction(reaction.emoji, user)

    def has_star_reaction(self):
        return '⭐' in [reaction.emoji for reaction in self.message.reactions]

    @abstractmethod
    def fetch_post(self):
        """
        Abstract method to fetch a post, should return `AbstractPostData`
        Method should set `self.post_data`
        """
        pass
