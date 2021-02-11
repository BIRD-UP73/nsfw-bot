import collections

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

max_len = 20


class PostHist(commands.Cog):
    post_list = collections.deque(maxlen=max_len)

    @commands.command(name='history', aliases=['hist'], brief='Post history')
    async def post_history(self, ctx: Context):
        embed = Embed()
        embed.title = 'History'

        embed.add_field(name='Posts', value='\n'.join(self.post_list))
        await ctx.send(embed=embed)

    def add_post(self, url: str):
        self.post_list.append(url)
