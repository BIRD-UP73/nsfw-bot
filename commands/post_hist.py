from collections import deque
from typing import Union, Dict, List

from discord import Embed, DMChannel, Guild
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from util.embed_util import PageData, PageEmbedMessage

max_len = 20


class PostHistData(PageData):
    def __init__(self, urls: List[str]):
        self.urls = urls

    def to_content(self) -> dict:
        embed = Embed()
        embed.add_field(name=f'Posts', value='\n'.join(self.urls))
        return {'embed': embed}


class PostHistMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, data: List[PostHistData]):
        super().__init__(ctx, data)

    async def on_reaction_add(self, reaction, user):
        await super().on_reaction_add(reaction, user)

        if user == self.ctx.bot.user or self.message.id != reaction.message.id:
            return
        if reaction.emoji == '🗑️':
            await self.message.delete()
            self.ctx.bot.remove_listener(self.on_reaction_add)
        elif self.ctx.guild:
            await self.message.remove_reaction(reaction.emoji, user)

    async def update_message(self):
        await self.message.edit(**self.to_content())

    def to_content(self) -> dict:
        page_data = self.data[self.page]
        content = page_data.to_content()

        print(content)

        if embed := content.get('embed'):
            embed.title = 'History'
            embed.description = f'Page {self.page + 1} of {len(self.data)}'
            content['embed'] = embed

        return content


class PostHist(commands.Cog):
    post_hist: Dict[int, deque] = dict()

    @is_nsfw()
    @commands.command(name='history', aliases=['hist'], brief='Post history')
    async def post_history(self, ctx: Context):
        channel_hist = self.get_hist(ctx.channel.id)

        if not channel_hist:
            return await ctx.send(content='No history')

        parsed_posts = []
        post_data_list = []

        for url in list(channel_hist):
            joined_txt = '\n'.join(parsed_posts)

            if len(joined_txt) + len(url) > 1024:
                post_data_list.append(PostHistData(parsed_posts))
                parsed_posts = []
            else:
                parsed_posts.append(url)

        post_data_list.append(PostHistData(parsed_posts))

        post_hist_message = PostHistMessage(ctx, post_data_list)
        await post_hist_message.create_message()

    def add_post(self, guild_or_channel: Union[Guild, DMChannel], url: str):
        self.post_hist.setdefault(guild_or_channel.id, deque(maxlen=max_len))
        self.post_hist[guild_or_channel.id].append(url)

    def get_hist(self, channel_or_guild_id: int):
        return self.post_hist.get(channel_or_guild_id)
