from abc import abstractmethod
from datetime import datetime
from typing import Union, Optional, List

from discord import User, Member, Reaction
from discord.ext.commands import Context

from posts.data.post_data import PostData, DisallowedTagsPost
from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class PostMessage(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx)
        self.url: str = url
        self.tags: str = tags
        self.post_data: Optional[PostData] = None
        self.page = 0

    async def create_message(self):
        self.fetch_random_post()
        await super().create_message()

    @property
    def emojis(self) -> List[str]:
        return super().emojis + ['🔁']

    async def update_message(self):
        await self.message.edit(**self.page_content().to_dict())

    async def delete_message(self, deleting_user: User):
        if deleting_user.id == self.author.id:
            return await super().delete_message(deleting_user)

        return True

    def update_hist(self, post_data: PostData):
        """
        Adds the current post to the post history
        """
        hist_cog = self.bot.get_cog('PostHist')
        hist_cog.add_to_history(self.channel, self.url, post_data)

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> Optional[bool]:
        result = await super().handle_reaction(reaction, user)

        if result is not None:
            return result

        if reaction.emoji == '🔁':
            if user == self.author:
                self.fetch_random_post()
                await self.update_message()
            return True
        if reaction.emoji == '⭐':
            await self.add_favorite(user)
            return True

    def to_post_entry(self) -> PostEntry:
        return PostEntry(self.url, self.post_data.post_id, datetime.now(), self.post_data)

    def get_post(self) -> PostData:
        if self.post_data.has_disallowed_tags():
            return DisallowedTagsPost()

        self.update_hist(self.post_data)
        return self.post_data

    def page_content(self) -> PostMessageContent:
        return self.get_post().to_message_content()

    @abstractmethod
    def fetch_random_post(self):
        """
        Abstract method to fetch a post, should return :class:`PostData`
        """
        pass
