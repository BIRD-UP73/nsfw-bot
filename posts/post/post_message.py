from abc import abstractmethod
from datetime import datetime
from typing import Union, Optional

from discord import User, Member, Reaction
from discord.ext.commands import Context

from posts.data.post_data import PostData, PostHasDisallowedTags
from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.message.reaction_handler import add_favorite
from posts.post.abstract_post import AbstractPost


class PostMessage(AbstractPost):
    emojis = ['🔁', '⭐', '🗑️']

    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx)
        self.url: str = url
        self.tags: str = tags
        self.post_data: Optional[PostData] = None

    async def update_message(self):
        self.post_data = self.fetch_post()
        post_content = self.post_data.to_message_content()
        await self.message.edit(**post_content.to_dict())
        return True

    def update_hist(self, post_data: PostData):
        """
        Adds the current post to the post history
        """
        hist_cog = self.bot.get_cog('PostHist')
        hist_cog.add_to_history(self.channel, self.url, post_data)

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> bool:
        if reaction.emoji == '🔁':
            if user == self.author:
                return await self.update_message()
            return True
        if reaction.emoji == '⭐':
            return await self.add_favorite(user)
        if reaction.emoji == '🗑️':
            if user == self.author:
                return await self.remove_message()
            return True

    async def add_favorite(self, user: User) -> bool:
        add_favorite(user, PostEntry(self.url, self.post_data.post_id, datetime.now(), self.post_data))
        await self.channel.send(f'{user.mention}, succesfully added favorite.')
        return True

    def get_post(self) -> PostData:
        post_data = self.fetch_post()
        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data

    def page_content(self) -> PostMessageContent:
        self.post_data = self.get_post()
        return self.fetch_post().to_message_content()

    @abstractmethod
    def fetch_post(self) -> PostData:
        """
        Abstract method to fetch a post, should return :class:`PostData`
        """
        pass
