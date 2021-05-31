from datetime import datetime
from typing import Union, Optional, List

from discord import Reaction, Member, Message, DMChannel, TextChannel, RawReactionActionEvent, Color
from discord.abc import User
from discord.ext.commands import Context, Bot

from db import post_repository
from posts.data.post_data import ErrorPost
from posts.events.favorite_event import FavoriteEvent
from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.fetcher.post_fetcher import PostFetcher
from posts.post_entry import PostEntry
from posts.post_message.post_message_content import MessageContent


class PostMessage:
    def __init__(self, fetcher: Union[PostFetcher, PostEntryFetcher], ctx: Context, emojis: List[str]):
        self.fetcher: PostFetcher = fetcher
        self.author: Union[User, Member] = ctx.author
        self.bot: Bot = ctx.bot
        self.channel: Union[TextChannel, DMChannel] = ctx.channel
        self.emojis: List[str] = emojis
        self.original_message: Message = ctx.message
        self.message: Optional[Message] = None

    async def create_message(self):
        self.fetcher.fetch_count()
        self.fetcher.fetch_current_page(self.channel)

        self.message = await self.channel.send(**self.page_content().to_dict())

        if self.original_message.guild:
            await self.original_message.delete()

        if self.message.guild:
            self.bot.add_listener(self.on_reaction_add)
        else:
            self.bot.add_listener(self.on_raw_reaction_add)

        await self.add_reactions()

    async def add_reactions(self):
        for emoji in self.emojis:
            await self.message.add_reaction(emoji)

    async def on_raw_reaction_add(self, event: RawReactionActionEvent):
        """
        This listener is used for DMs to bypass having to use member intents
        """
        message = await self.channel.fetch_message(event.message_id)
        reaction_data = dict(me=False, count=0)
        reaction = Reaction(message=message, data=reaction_data, emoji=str(event.emoji))

        user = await self.bot.fetch_user(event.user_id)

        await self.on_reaction_add(reaction, user)

    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        if user.id == self.bot.user.id or self.message.id != reaction.message.id:
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
            await self.message.delete()
            return False

        if reaction.emoji == '🔁':
            self.fetcher.paginator.random_page()
        if reaction.emoji == '➡':
            self.fetcher.paginator.next_page()
        if reaction.emoji == '⬅':
            self.fetcher.paginator.previous_page()

        self.fetcher.fetch_current_page(self.channel)
        await self.update_message()
        return True

    async def add_favorite(self, user: User):
        if post_repository.store_favorite(user, self.fetcher.get_post()):
            await self.channel.send(f'{user.mention}, successfully stored favorite.')

        new_entry = PostEntry(self.fetcher.url, self.fetcher.get_post().post_id, datetime.now())
        self.bot.dispatch('favorite_add', FavoriteEvent(new_entry, user))

    async def update_message(self):
        content = self.generic_display().to_dict()
        await self.message.edit(**content)

    def page_content(self) -> MessageContent:
        """
        Returns the content of the current page of the embed
        This should be in the form of a :type mapping: dict
        with both a 'content' and an 'embed' field

        :return: the content of the page
        """
        return self.generic_display()

    def generic_display(self) -> MessageContent:
        post = self.fetcher.get_post()

        if not post:
            return self.error_content(MessageContent(), None)

        message_content = post.to_message_content()

        message_content.page = self.fetcher.paginator.display_page()
        message_content.total_pages = self.fetcher.paginator.post_count

        if isinstance(post, ErrorPost):
            return self.error_content(message_content, post)

        return self.success_content(message_content)

    def error_content(self, message_content: MessageContent, error_post: Optional[ErrorPost]) -> MessageContent:
        message_content.color = Color.red()
        message_content.add_field(name='Error', value=error_post.message)
        return message_content

    def success_content(self, message_content: MessageContent) -> MessageContent:
        return message_content
