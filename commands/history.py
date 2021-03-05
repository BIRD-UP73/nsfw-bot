from collections import deque
from datetime import datetime
from typing import Union, Dict, List, Deque

from discord import DMChannel, TextChannel
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from posts.data.post_entry import PostEntry
from posts.message.page_embed_message import PageEmbedMessage
from posts.message.reaction_handler import DeleteMessageReactionHandler
from util.url_util import parse_url


class PostHistMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, data: List[PostEntry]):
        super().__init__(ctx, data)
        self.reaction_handlers['🗑️'] = DeleteMessageReactionHandler()

    def get_current_page(self) -> dict:
        entry_data = self.get_data()
        self.post_data = entry_data.fetch_post()

        if self.post_data.is_animated():
            return self.post_data.to_content()

        embed = self.post_data.to_embed()
        embed.title = 'History'
        embed.description = f'Page **{self.page + 1}** of **{len(self.data)}**'

        embed.timestamp = entry_data.saved_at

        return dict(content=None, embed=embed)


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

        post_hist_message = PostHistMessage(ctx, list(channel_hist))
        await post_hist_message.create_message()

    def add_to_history(self, channel: Union[TextChannel, DMChannel], url: str, post_id: int):
        self.post_hist.setdefault(channel.id, deque(maxlen=self.max_len))

        short_url = parse_url(url)
        post_hist_entry = PostEntry(short_url, post_id, datetime.now())
        self.post_hist[channel.id].append(post_hist_entry)
