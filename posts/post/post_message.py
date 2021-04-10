from typing import Optional

from discord import User
from discord.ext.commands import Context

from posts.data.post_data import Post
from posts.fetcher.post_fetcher import PostFetcher
from posts.message.post_message_content import PostMessageContent
from posts.paginator.paginator import Paginator
from posts.post.abstract_post import AbstractPostMessage


class PostMessage(AbstractPostMessage):
    def __init__(self, fetcher: PostFetcher, ctx: Context, paginator: Paginator = None):
        self.fetcher = fetcher
        super().__init__(fetcher, ctx, paginator)
        self.post_data: Optional[Post] = None

    async def delete_message(self, deleting_user: User):
        if deleting_user.id == self.author.id:
            return await super().delete_message(deleting_user)

        return True

    def page_content(self) -> PostMessageContent:
        message_content = self.fetcher.get_post().to_message_content()

        if embed := message_content.embed:
            embed.description = f'Post **{self.paginator.page}** of **{self.paginator.post_count}**'

        return message_content
