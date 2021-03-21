from collections import deque
from datetime import datetime
from typing import Union, Dict, Deque

from discord import DMChannel, TextChannel
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from posts.data.post_data import PostData
from posts.data.post_entry import PostEntry
from posts.message.page_embed_message import PageEmbedMessage
from posts.message.post_message_content import PostMessageContent
from util.url_util import parse_url


class HistoryMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, data: Deque[PostEntry]):
        super().__init__(ctx, data)

    def page_content(self) -> PostMessageContent:
        entry_data = self.to_post_entry()
        post_data = entry_data.fetch_post()

        message_content = post_data.to_message_content()

        if message_content.embed:
            message_content.embed.title = 'History'
            message_content.embed.description = f'Page **{self.page + 1}** of **{len(self.data)}**'

            message_content.embed.timestamp = entry_data.saved_at

        return message_content


class PostHist(commands.Cog):
    max_len = 50
    post_hist: Dict[int, Deque[PostEntry]] = {}

    description = """
    ⭐   add post to your favorites
    🗑️  remove message
    ⬅➡ scroll through pages
    """

    @is_nsfw()
    @commands.command(name='history', aliases=['hist'], brief='Post history', description=description)
    async def post_history(self, ctx: Context):
        channel_hist = self.post_hist.get(ctx.channel.id)

        if not channel_hist:
            return await ctx.send('No history')

        await HistoryMessage(ctx, channel_hist).create_message()

    def add_to_history(self, channel: Union[TextChannel, DMChannel], url: str, post_data: PostData):
        self.post_hist.setdefault(channel.id, deque(maxlen=self.max_len))

        short_url = parse_url(url)
        post_hist_entry = PostEntry(short_url, post_data.post_id, datetime.now(), post_data)

        self.post_hist[channel.id].append(post_hist_entry)
