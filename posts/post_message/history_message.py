from datetime import datetime
from typing import List

from discord.ext.commands import Context

from posts.events.history_event import HistoryEvent
from posts.post_entry import PostEntry
from posts.post_message.list_message import ListMessage
from posts.post_message.post_message_content import MessageContent


class HistoryMessage(ListMessage):
    def __init__(self, ctx: Context, data: List[PostEntry], emojis: List[str]):
        super().__init__(ctx, data, emojis)

    async def create_message(self):
        await super().create_message()
        self.bot.add_listener(self.on_history_add)

    async def on_history_add(self, event: HistoryEvent):
        entry = PostEntry(event.post.board_url, event.post.post_id, datetime.now())

        if self.channel.id == event.source.id and entry not in self.fetcher.data:
            self.fetcher.data.append(entry)
            self.fetcher.fetch_count()
            self.fetcher.fetch_current_page(event.source, False)

            if self.message:
                await self.update_message()

    def generic_display(self) -> MessageContent:
        message_content = super().generic_display()
        message_content.title = 'Post history'

        return message_content
