from collections import deque
from typing import Union, Dict

from discord import Embed, DMChannel, Guild
from discord.ext import commands
from discord.ext.commands import Context

max_len = 20


class PostHist(commands.Cog):
    post_hist: Dict[int, deque] = dict()

    @commands.command(name='history', aliases=['hist'], brief='Post history')
    async def post_history(self, ctx: Context):
        channel_hist = self.get_hist(ctx.channel.id)

        if not channel_hist:
            return await ctx.send(content='No history')

        embed = Embed()
        embed.title = 'History'

        embed.add_field(name='Posts 1', value='\n'.join(list(channel_hist)[:10]))
        posts_2 = list(channel_hist)[10:]

        if posts_2:
            embed.add_field(name='Posts 2', value='\n'.join(posts_2))

        await ctx.send(embed=embed)

    def add_post(self, guild_or_channel: Union[Guild, DMChannel], url: str):
        self.post_hist.setdefault(guild_or_channel.id, deque(maxlen=max_len))
        self.post_hist[guild_or_channel.id].append(url)

    def get_hist(self, channel_or_guild_id: int):
        return self.post_hist.get(channel_or_guild_id)
