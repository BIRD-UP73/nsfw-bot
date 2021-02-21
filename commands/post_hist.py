from collections import deque
from typing import Union, Dict

from discord import Embed, DMChannel, Guild
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

max_len = 20


class PostHist(commands.Cog):
    post_hist: Dict[int, deque] = dict()

    @is_nsfw()
    @commands.command(name='history', aliases=['hist'], brief='Post history')
    async def post_history(self, ctx: Context):
        channel_hist = self.get_hist(ctx.channel.id)

        if not channel_hist:
            return await ctx.send(content='No history')

        embed = Embed()
        embed.title = 'History'

        post_list = list(channel_hist)

        parsed_posts = []
        post_idx = 1

        for url in post_list:
            joined_txt = '\n'.join(parsed_posts)

            if len(joined_txt) + len(url) > 1024:
                embed.add_field(name=f'Posts {post_idx}', value=joined_txt)
                post_idx += 1
                parsed_posts = []
            else:
                parsed_posts.append(url)

        if len(parsed_posts) > 0:
            embed.add_field(name=f'Posts {post_idx}', value='\n'.join(parsed_posts))

        await ctx.send(embed=embed)

    def add_post(self, guild_or_channel: Union[Guild, DMChannel], url: str):
        self.post_hist.setdefault(guild_or_channel.id, deque(maxlen=max_len))
        self.post_hist[guild_or_channel.id].append(url)

    def get_hist(self, channel_or_guild_id: int):
        return self.post_hist.get(channel_or_guild_id)
