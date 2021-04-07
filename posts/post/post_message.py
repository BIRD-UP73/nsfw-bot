from typing import Optional

from discord import User
from discord.ext.commands import Context

from posts.data.post_data import PostData
from posts.fetcher.post_fetcher import PostFetcher
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class PostMessage(AbstractPost):
    def __init__(self, fetcher: PostFetcher, ctx: Context):
        self.fetcher = fetcher
        super().__init__(fetcher, ctx)
        self.post_data: Optional[PostData] = None

    async def delete_message(self, deleting_user: User):
        if deleting_user.id == self.author.id:
            return await super().delete_message(deleting_user)

        return True

    def page_content(self) -> PostMessageContent:
        message_content = self.fetcher.get_post().to_message_content()

        if message_content.embed:
            message_content.embed.description = f'Post **{self.fetcher.current_page()}**' \
                                                f' of **{self.fetcher.post_count()}**'

        return message_content
