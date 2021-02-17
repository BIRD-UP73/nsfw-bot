from abc import ABC, abstractmethod

from discord import Reaction, User, Embed, Message, Color
from discord.ext.commands import Context

import util


class AbstractPostData(ABC):
    tags: str = None

    @abstractmethod
    def to_content(self) -> dict:
        pass

    def has_disallowed_tags(self):
        return util.contains_disallowed_tags(self.tags)


class PostError(AbstractPostData):
    """
    Post used to indicate something went wrong
    """
    def __init__(self, message: str):
        self.message = message

    @property
    def tags(self) -> str:
        return ''

    def to_content(self) -> dict:
        embed = Embed()
        embed.title = 'Error'
        embed.description = self.message

        embed.colour = Color.red()

        return {'content': None, 'embed': embed}


class AbstractPost(ABC):
    ctx: Context = None
    msg: Message = None
    post_data: AbstractPostData = None
    url: str = None
    tags: str = None

    async def create_message(self):
        post_data = self.fetch_post()
        self.msg = await self.ctx.send(**post_data.to_content())

        self.ctx.bot.add_listener(self.on_reaction_add)
        await self.msg.add_reaction('🗑️')
        await self.msg.add_reaction('🔁')

    def update_hist(self, post_data):
        """
        Adds the current post to the post history
        """
        hist_cog = self.ctx.bot.get_cog('PostHist')
        hist_cog.add_post(self.ctx.channel, post_data.file_url)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        if reaction.message.id != self.msg.id or user == self.ctx.bot.user:
            return
        if reaction.emoji == '🗑️':
            await self.msg.delete()
            self.ctx.bot.remove_listener(self.on_reaction_add)
            return

        if reaction.emoji == '🔁':
            post_data = self.fetch_post()
            await self.msg.edit(**post_data.to_content())

        if self.ctx.guild:
            await self.msg.remove_reaction(reaction.emoji, user)

    @abstractmethod
    def fetch_post(self) -> AbstractPostData:
        """
        Abstract method to fetch a post, should return `AbstractPostData`
        :return: post data
        """
        pass
