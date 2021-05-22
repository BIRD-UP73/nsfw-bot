from typing import List

from discord import User, Color
from discord.ext.commands import Context

from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.paginator.paginator import Paginator
from posts.post_entry import PostEntry
from posts.post_message.post_message import PostMessage
from posts.post_message.post_message_content import MessageContent


class ListMessage(PostMessage):
    def __init__(self, ctx: Context, data: List[PostEntry], emojis: List[str]):
        self.fetcher: PostEntryFetcher = PostEntryFetcher(data, Paginator())
        super().__init__(self.fetcher, ctx, emojis)

    async def add_favorite(self, user: User):
        if len(self.fetcher.data) > 0:
            await super().add_favorite(user)

    def page_content(self) -> MessageContent:
        if len(self.fetcher.data) == 0:
            return MessageContent(title='Error', description='No posts found.', color=Color.red())

        return super().page_content()
