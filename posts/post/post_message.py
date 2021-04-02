from abc import ABC
from datetime import datetime
from typing import Optional

from discord import User
from discord.ext.commands import Context, CommandError

from posts.data.post_data import PostData, DisallowedTagsPost
from posts.data.post_entry import PostEntry
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class PostMessage(AbstractPost, ABC):
    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx)
        self.url: str = url
        self.tags: str = tags
        self.post_data: Optional[PostData] = None

    async def create_message(self):
        self.fetch_total_posts()

        if self.total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

        self.fetch_post_for_page()
        await super().create_message()

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

    def to_post_entry(self) -> PostEntry:
        return PostEntry(self.url, self.post_data.post_id, datetime.now(), self.post_data)

    def get_post(self) -> PostData:
        if self.post_data.has_disallowed_tags():
            return DisallowedTagsPost()

        self.update_hist(self.post_data)
        return self.post_data

    def page_content(self) -> PostMessageContent:
        message_content = self.get_post().to_message_content()

        if message_content.embed:
            message_content.embed.description = f'Post **{self.page}** of **{self.total_posts}**'

        return message_content
