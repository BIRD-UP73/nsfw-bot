from typing import List

from discord.ext.commands import Context

from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.paginator.paginator import Paginator
from posts.post_entry import PostEntry
from posts.post_message.post_message import PostMessage
from posts.post_message.post_message_content import MessageContent


class HistoryMessage(PostMessage):
    def __init__(self, ctx: Context, data: List[PostEntry], emojis: List[str]):
        paginator = Paginator()
        self.fetcher = PostEntryFetcher(data, paginator)
        super().__init__(self.fetcher, ctx, emojis, paginator)

    def page_content(self) -> MessageContent:
        post_data = self.fetcher.get_post()
        message_content = post_data.to_message_content()

        if embed := message_content.embed:
            embed.title = 'Post history'
            embed.description = f'Page **{self.paginator.page + 1}** of **{self.paginator.post_count}**'
            embed.timestamp = self.fetcher.current_entry().saved_at
            embed.set_footer(text=f'Page {self.paginator.page + 1} of {self.paginator.post_count}'
                                  f' • Score: {post_data.score}')

        return message_content
