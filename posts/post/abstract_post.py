from abc import abstractmethod, ABC
from typing import Union, Optional

from discord import Reaction, Member, Message
from discord.abc import User, Messageable
from discord.ext.commands import Context, Bot

from posts.message.post_message_content import PostMessageContent


class AbstractPost(ABC):
    emojis = ['🗑️', '⭐']

    def __init__(self, ctx: Context):
        self.author: Union[User, Member] = ctx.author
        self.bot: Bot = ctx.bot
        self.channel: Union[Messageable] = ctx.channel
        self.message: Optional[Message] = None

    async def create_message(self):
        page_content = self.page_content()
        self.message = await self.channel.send(**page_content.to_dict())

        self.bot.add_listener(self.on_reaction_add)
        await self.add_emojis()

    async def add_emojis(self):
        for emoji in self.emojis:
            await self.message.add_reaction(emoji)

    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        if user == self.bot.user or self.message.id != reaction.message.id:
            return

        delete_reaction = await self.handle_reaction(reaction, user)

        if delete_reaction and self.message.guild:
            await self.message.remove_reaction(reaction.emoji, user)

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> Optional[bool]:
        """
        :return: whether the reaction should be deleted after
        """
        if reaction.emoji not in self.emojis:
            return True

        if reaction.emoji == '⭐':
            return await self.add_favorite(user)

    async def remove_message(self) -> bool:
        await self.message.delete()
        return False

    @abstractmethod
    async def add_favorite(self, user: User) -> bool:
        pass

    @abstractmethod
    def page_content(self) -> PostMessageContent:
        """
        Returns the content of the current page of the embed
        This should be in the form of a :type mapping: dict
        with both a 'content' and an 'embed' field

        :return: the content of the page
        """
        pass
