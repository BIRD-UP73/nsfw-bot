from collections import deque
from datetime import datetime
from typing import Union, Dict, List, Deque

from discord import DMChannel, Guild
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from api.post_entry import PostEntry
from api.page_embed_message import PageEmbedMessage
from util.url_util import parse_url


class PostHistEntry(PostEntry):
    def __init__(self, url: str, post_id: int, saved_at: datetime):
        super().__init__(url, post_id)
        self.saved_at = saved_at


class PostHistMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, data: List[PostHistEntry]):
        super().__init__(ctx, data)

    async def on_reaction_add(self, reaction, user):
        if user == self.ctx.bot.user or self.message.id != reaction.message.id:
            return

        await super().on_reaction_add(reaction, user)

        if reaction.emoji == '🗑️':
            await self.message.delete()
            self.ctx.bot.remove_listener(self.on_reaction_add)
        else:
            await super().after_reaction(reaction, user)

    def get_current_page(self) -> dict:
        entry_data = self.get_data()
        post_data = entry_data.fetch_post()

        if post_data.is_animated():
            return post_data.to_content()

        embed = post_data.to_embed()
        embed.title = 'History'

        embed.set_footer(text=f'Page {self.page + 1} of {len(self.data)}')
        embed.timestamp = entry_data.saved_at

        return dict(content=None, embed=embed)


class PostHist(commands.Cog):
    max_len = 50
    post_hist: Dict[int, Deque[PostHistEntry]] = dict()

    description = """
    ⭐   add post to your favorites
    🗑️  remove message
    ⬅➡ scroll through pages
    """

    @is_nsfw()
    @commands.command(name='history', aliases=['hist'], brief='Post history', description=description)
    async def post_history(self, ctx: Context):
        channel_hist = self.get_hist(ctx.guild or ctx.channel)

        if not channel_hist:
            return await ctx.send(content='No history')

        post_hist_message = PostHistMessage(ctx, list(channel_hist))
        await post_hist_message.create_message()

    def add_post(self, guild_or_channel: Union[Guild, DMChannel], url: str, post_id: int):
        self.post_hist.setdefault(guild_or_channel.id, deque(maxlen=self.max_len))

        short_url = parse_url(url)
        post_hist_entry = PostHistEntry(short_url, post_id, datetime.now())
        self.post_hist[guild_or_channel.id].append(post_hist_entry)

    def get_hist(self, guild_or_channel: Union[Guild, DMChannel]) -> Deque[PostHistEntry]:
        return self.post_hist.get(guild_or_channel.id)
