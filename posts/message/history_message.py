from typing import List

from discord.ext.commands import Context

from posts.data.post_entry import PostEntry
from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.message.post_message_content import PostMessageContent
from posts.paginator.paginator import DefaultPaginator
from posts.post.abstract_post import AbstractPostMessage


class HistoryMessage(AbstractPostMessage):
    def __init__(self, ctx: Context, data: List[PostEntry]):
        paginator = DefaultPaginator()
        self.fetcher = PostEntryFetcher(data, paginator)
        super().__init__(self.fetcher, ctx, paginator)

    def page_content(self) -> PostMessageContent:
        post_data = self.fetcher.get_post()
        message_content = post_data.to_message_content()

        if embed := message_content.embed:
            embed.title = 'Post history'
            embed.description = f'Page **{self.paginator.page + 1}** of **{self.paginator.post_count}**'
            embed.timestamp = self.fetcher.current_entry().saved_at
            embed.set_footer(text=f'Page {self.paginator.page + 1} of {self.paginator.post_count}'
                                  f' • Score: {post_data.score}')

        return message_content
