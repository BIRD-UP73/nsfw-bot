from typing import List

from discord.ext.commands import Context

from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.paginator.paginator import Paginator
from posts.post_entry import PostEntry
from posts.post_message.post_message import PostMessage
from posts.post_message.post_message_content import MessageContent


class HistoryMessage(PostMessage):
    def __init__(self, ctx: Context, data: List[PostEntry], emojis: List[str]):
        self.fetcher: PostEntryFetcher = PostEntryFetcher(data, Paginator())
        super().__init__(self.fetcher, ctx, emojis)

    def page_content(self) -> MessageContent:
        message_content = super().page_content()

        if embed := message_content.embed:
            embed.title = 'Post history'

        return message_content
