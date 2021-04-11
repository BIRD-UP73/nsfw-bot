from abc import ABC, abstractmethod
from typing import Union, Optional, List

from discord import Reaction, Member, Message, DMChannel, TextChannel
from discord.abc import User
from discord.ext.commands import Context, Bot, UserInputError

from db import post_repository
from posts.fetcher.abstract_post_fetcher import AbstractPostFetcher
from posts.post_message.post_message_content import PostMessageContent
from posts.paginator.paginator import Paginator


class AbstractPostMessage(ABC):
    def __init__(self, fetcher: AbstractPostFetcher, ctx: Context, paginator=None):
        self.fetcher: AbstractPostFetcher = fetcher
        self.author: Union[User, Member] = ctx.author
        self.bot: Bot = ctx.bot
        self.channel: Union[TextChannel, DMChannel] = ctx.channel
        self.paginator: Paginator = paginator or Paginator()
        self.message: Optional[Message] = None

    @property
    def emojis(self) -> List[str]:
        return ['⭐', '⬅', '➡', '🔁', '🗑️']

    @staticmethod
    def is_page_emoji(emoji: str) -> bool:
        return emoji in ['⬅', '➡', '🔁']

    async def create_message(self):
        self.paginator.post_count = self.fetcher.fetch_count()

        if self.paginator.post_count == 0:
            raise UserInputError('No posts found.')

        self.fetcher.fetch_for_page(self.paginator.page, self.channel)

        self.message = await self.channel.send(**self.page_content().to_dict())

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
            await self.add_favorite(user)
            return True

        # Ignore non-author reactions below
        if user != self.author:
            return True

        if reaction.emoji == '🗑️':
            return await self.message.delete()

        if self.is_page_emoji(reaction.emoji):
            if reaction.emoji == '🔁':
                self.paginator.random_page()
            if reaction.emoji == '➡':
                self.paginator.next_page()
            if reaction.emoji == '⬅':
                self.paginator.previous_page()

            self.fetcher.fetch_for_page(self.paginator.page, self.channel)
            await self.update_message()
            return True

    async def add_favorite(self, user: User):
        if post_repository.store_favorite(user, self.fetcher.get_post()):
            await self.channel.send(f'{user.mention}, successfully stored favorite.')

    async def update_message(self):
        await self.message.edit(**self.page_content().to_dict())

    @abstractmethod
    def page_content(self) -> PostMessageContent:
        """
        Returns the content of the current page of the embed
        This should be in the form of a :type mapping: dict
        with both a 'content' and an 'embed' field

        :return: the content of the page
        """
        pass