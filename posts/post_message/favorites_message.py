from datetime import datetime
from typing import List, Union, Optional

from discord import User, Reaction, Member
from discord.ext.commands import Context

from db import post_repository
from posts.events.favorite_event import FavoriteEvent
from posts.post_entry import PostEntry
from posts.post_message.list_message import ListMessage
from posts.post_message.post_message_content import MessageContent


class FavoritesMessage(ListMessage):
    def __init__(self, ctx: Context, data: List[PostEntry], emojis: List[str]):
        super().__init__(ctx, data, emojis)

    async def create_message(self):
        await super().create_message()

        self.bot.add_listener(self.on_favorite_add)
        self.bot.add_listener(self.on_favorite_remove)

    async def on_favorite_add(self, event: FavoriteEvent):
        if event.user.id == self.author.id and event.post_entry not in self.fetcher.data:
            self.fetcher.data.append(event.post_entry)
            self.fetcher.fetch_count()
            await self.update_message()

    async def on_favorite_remove(self, event: FavoriteEvent):
        if event.user.id == self.author.id and event.post_entry in self.fetcher.data:
            self.fetcher.remove_post(event.post_entry)
            self.fetcher.fetch_count()
            await self.update_message()

    async def add_favorite(self, user: User):
        if user != self.author:
            await super().add_favorite(user)

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> Optional[bool]:
        if reaction.emoji == '⛔':
            await self.remove_favorite(user)
            return True

        return await super().handle_reaction(reaction, user)

    async def remove_favorite(self, user: User):
        if user != self.author or len(self.fetcher.data) == 0:
            return

        old_post = self.fetcher.get_post()

        post_repository.remove_favorite(user, old_post)
        await self.channel.send(f'{user.mention}, removed favorite successfully.')
        self.fetcher.remove_post_for_page(self.fetcher.paginator.page)

        await self.update_message()

        removed_entry = PostEntry(old_post.board_url, old_post.post_id, datetime.now())
        self.bot.dispatch('favorite_remove', FavoriteEvent(removed_entry, user))

    async def update_message(self):
        if self.fetcher.paginator.post_count == 0:
            return await self.message.edit(content='No favorites.', embed=None)

        self.fetcher.fetch_for_page(self.fetcher.paginator.page, self.channel)
        await super().update_message()

    def page_content(self) -> MessageContent:
        message_content = super().page_content()

        message_content.title = 'Favorites'
        message_content.description = f'Favorites for {self.author.mention}'

        current_entry = self.fetcher.current_entry()
        message_content.timestamp = str(current_entry.saved_at)

        message_content.page = self.fetcher.paginator.display_page()
        message_content.post_count = self.fetcher.paginator.post_count

        return message_content
