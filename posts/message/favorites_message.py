from typing import List, Union, Optional

from discord import User, Reaction, Member
from discord.ext.commands import Context

from db import post_repository
from posts.data.post_entry import PostEntry
from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost
from util.url_util import parse_url


class FavoritesMessage(AbstractPost):
    def __init__(self, ctx: Context, data: List[PostEntry], user: User):
        self.fetcher = PostEntryFetcher(data)
        super().__init__(self.fetcher, ctx)
        self.user = user

    @property
    def emojis(self) -> List[str]:
        return super().emojis + ['⛔']

    async def add_favorite(self, user):
        if user != self.author:
            await super().add_favorite(user)

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> Optional[bool]:
        if reaction.emoji == '⛔':
            await self.remove_favorite(user)
            return True

        return await super().handle_reaction(reaction, user)

    async def remove_favorite(self, user: User):
        if user != self.user:
            return

        data = self.fetcher.get_post()

        post_repository.remove_favorite(user, parse_url(data.file_url), data.post_id)
        await self.channel.send(f'{user.mention}, removed favorite successfully.')
        self.fetcher.remove_post(self.page)

        if len(self.fetcher.data) == 0:
            return await self.clear_message()

        if self.page == len(self.fetcher.data):
            self.fetcher.page = 0

        await self.update_message()

    def page_content(self) -> PostMessageContent:
        post_data = self.fetcher.get_post()
        message_content = post_data.to_message_content()

        if message_content.embed is not None:
            message_content.embed.title = 'Favorites'
            message_content.embed.description = f'Favorites for {self.user.mention}'
            message_content.embed.timestamp = self.fetcher.current_post_timestamp()
            message_content.embed.set_footer(text=f'Page {self.fetcher.paginator.page + 1}'
                                                  f' of {len(self.fetcher.data)}')

        return message_content

    async def clear_message(self):
        self.bot.remove_listener(self.on_reaction_add)
        await self.message.clear_reactions()
        await self.message.edit(content='No favorites.', embed=None)
