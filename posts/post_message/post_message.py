from discord.ext.commands import Context

from posts.fetcher.post_fetcher import PostFetcher
from posts.post_message.post_message_content import PostMessageContent
from posts.paginator.paginator import Paginator
from posts.post_message.abstract_post_message import AbstractPostMessage


class PostMessage(AbstractPostMessage):
    def __init__(self, fetcher: PostFetcher, ctx: Context, paginator: Paginator = None):
        self.fetcher = fetcher
        super().__init__(fetcher, ctx, paginator)

    def page_content(self) -> PostMessageContent:
        message_content = self.fetcher.get_post().to_message_content()

        if embed := message_content.embed:
            embed.description = f'Post **{self.paginator.page}** of **{self.paginator.post_count}**'

        return message_content
