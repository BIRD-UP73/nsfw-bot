from collections import deque
from datetime import datetime
from typing import Union, Dict, Deque

from discord import DMChannel, TextChannel
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from posts.data.post_entry import PostEntry
from posts.message.page_embed_message import PageEmbedMessage
from posts.message.reaction_handler import DeleteMessageReactionHandler
from posts.post.post_fetcher import PostEntryFetcher
from util.url_util import parse_url


class PostHistMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, fetcher: PostEntryFetcher):
        super().__init__(ctx, fetcher)
        self.reaction_handlers['🗑️'] = DeleteMessageReactionHandler()

    def get_current_page(self) -> dict:
        post_data = self.fetcher.fetch_post()

        if post_data.is_animated():
            return dict(content=post_data.to_text(), embed=None)

        embed = post_data.to_embed()
        embed.title = 'History'
        embed.description = f'Page **{self.fetcher.page + 1}** of **{len(self.fetcher.entries)}**'

        entry = self.fetcher.current_entry()
        embed.timestamp = entry.saved_at

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

        post_hist_fetcher = PostEntryFetcher(list(channel_hist))
        post_hist_message = PostHistMessage(ctx, post_hist_fetcher)
        await post_hist_message.create_message()

    def add_to_history(self, channel: Union[TextChannel, DMChannel], url: str, post_id: int):
        self.post_hist.setdefault(channel.id, deque(maxlen=self.max_len))

        short_url = parse_url(url)
        post_hist_entry = PostEntry(short_url, post_id, datetime.now())
        self.post_hist[channel.id].append(post_hist_entry)
