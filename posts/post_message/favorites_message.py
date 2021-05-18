from datetime import datetime
from typing import List, Union, Optional

from discord import User, Reaction, Member
from discord.ext.commands import Context

from db import post_repository
from posts.events.favorite_event import FavoriteEvent
from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.paginator.paginator import Paginator
from posts.post_entry import PostEntry
from posts.post_message.post_message import PostMessage
from posts.post_message.post_message_content import MessageContent


class FavoritesMessage(PostMessage):
    def __init__(self, ctx: Context, data: List[PostEntry], emojis: List[str]):
        self.fetcher: PostEntryFetcher = PostEntryFetcher(data,  Paginator())
        super().__init__(self.fetcher, ctx, emojis)

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
            self.fetcher.data.remove(event.post_entry)
            self.fetcher.fetch_count()

            if self.fetcher.paginator.post_count == 0:
                await self.clear_message()
            else:
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
        if user != self.author:
            return

        old_post = self.fetcher.get_post()

        post_repository.remove_favorite(user, old_post)
        await self.channel.send(f'{user.mention}, removed favorite successfully.')
        self.fetcher.remove_post(self.fetcher.paginator.page)

        if self.fetcher.paginator.post_count == 0:
            return await self.clear_message()

        self.fetcher.fetch_for_page(self.fetcher.paginator.page, self.channel)
        await self.update_message()

        removed_entry = PostEntry(old_post.board_url, old_post.post_id, datetime.now())
        self.bot.dispatch('favorite_remove', FavoriteEvent(removed_entry, user))

    async def clear_message(self):
        self.bot.remove_listener(self.on_reaction_add)
        await self.message.clear_reactions()
        await self.message.edit(content='No favorites.', embed=None)

    def page_content(self) -> MessageContent:
        post_data = self.fetcher.get_post()
        message_content = post_data.to_message_content()

        if embed := message_content.embed:
            embed.title = 'Favorites'
            embed.description = f'Favorites for {self.author.mention}'
            embed.timestamp = self.fetcher.current_entry().saved_at

            page = self.fetcher.paginator.display_page()
            post_count = self.fetcher.paginator.post_count

            embed.set_footer(text=f'Page {page} of {post_count} • Score: {post_data.score}')

        return message_content
