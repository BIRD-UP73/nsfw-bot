import random
from abc import abstractmethod, ABC
from typing import Union, Optional, List

from discord import Reaction, Member, Message
from discord.abc import User, Messageable
from discord.ext.commands import Context, Bot

from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.message.reaction_handler import add_favorite


class AbstractPost(ABC):
    def __init__(self, ctx: Context):
        self.author: Union[User, Member] = ctx.author
        self.bot: Bot = ctx.bot
        self.channel: Union[Messageable] = ctx.channel
        self.message: Optional[Message] = None
        self.page = 0
        self.total_posts = 0

    @property
    def emojis(self) -> List[str]:
        return ['⭐', '⬅', '➡', '🔁', '🗑️']

    async def create_message(self):
        self.fetch_total_posts()

        page_content = self.page_content()
        self.message = await self.channel.send(**page_content.to_dict())

        self.bot.add_listener(self.on_reaction_add)
        await self.add_emojis()

        listener_cog = self.bot.get_cog('Listeners')
        listener_cog.add_post(self)

    async def delete_message(self, deleting_user: User) -> bool:
        """
        Deletes the message belonging to the post

        :param deleting_user: the user that wants to delete the message
        :return: whether the reaction should be deleted
        """
        # Ignore deleting user here (anyone allowed to delete)
        await self.message.delete()
        return False

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
        if reaction.emoji == '🔁':
            if user == self.author:
                self.fetch_random_post()
                await self.update_message()
            return True
        if reaction.emoji == '➡':
            await self.next_page()
            return True
        if reaction.emoji == '⬅':
            await self.previous_page()
            return True
        if reaction.emoji == '🗑️':
            return await self.delete_message(user)

    async def add_favorite(self, user: User):
        if add_favorite(user, self.to_post_entry()):
            await self.channel.send(f'{user.mention}, successfully stored favorite.')

    async def update_message(self):
        page_content = self.page_content()
        await self.message.edit(**page_content.to_dict())

    def fetch_random_post(self):
        self.page = random.randint(0, self.total_posts - 1)
        self.fetch_post_for_page()

    async def next_page(self):
        self.page = (self.page + 1) % self.total_posts
        self.fetch_post_for_page()
        await self.update_message()

    async def previous_page(self):
        self.page = (self.page - 1) % self.total_posts
        self.fetch_post_for_page()
        await self.update_message()

    @abstractmethod
    def to_post_entry(self) -> PostEntry:
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

    @abstractmethod
    def fetch_post_for_page(self):
        pass

    @abstractmethod
    def fetch_total_posts(self):
        pass
