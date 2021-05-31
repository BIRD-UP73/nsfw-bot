from typing import List, Optional

from discord import User, Color
from discord.ext.commands import Context

from posts.data.post_data import ErrorPost
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

    def generic_display(self) -> MessageContent:
        message_content = super().generic_display()

        entry = self.fetcher.current_entry()

        if entry:
            message_content.timestamp = entry.saved_at

        return message_content

    def error_content(self, message_content: MessageContent, error_post: Optional[ErrorPost]) -> MessageContent:
        if not error_post:
            message = 'No posts found'
        else:
            message = error_post.message

        message_content.add_field(name='Error', value=message)
        message_content.color = Color.red()

        return message_content

    def success_content(self, message_content: MessageContent) -> MessageContent:
        message_content.file_url = self.fetcher.get_post().file_url
        return message_content
