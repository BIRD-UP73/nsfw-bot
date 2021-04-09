from typing import List

from discord.ext.commands import Context

from posts.data.post_entry import PostEntry
from posts.fetcher.post_entry_fetcher import PostEntryFetcher
from posts.message.post_message_content import PostMessageContent
from posts.post.abstract_post import AbstractPost


class HistoryMessage(AbstractPost):
    def __init__(self, ctx: Context, data: List[PostEntry]):
        self.fetcher = PostEntryFetcher(data)
        super().__init__(self.fetcher, ctx)

    def page_content(self) -> PostMessageContent:
        post_data = self.fetcher.get_post()
        message_content = post_data.to_message_content()

        if message_content.embed:
            message_content.title = 'History'
            message_content.description = f'Page **{self.fetcher.page + 1}** of **{len(self.fetcher.data)}**'
            message_content.timestamp = self.fetcher.current_entry().saved_at

        return message_content
