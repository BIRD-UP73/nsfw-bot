from typing import Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, NSFWChannelRequired, CommandError

from api import xml_api


class XmlPosts(commands.Cog):
    rule34_desc = """
    Searches images from rule34.xxx

    - For search terms, see https://rule34.xxx/index.php?page=help&topic=cheatsheet
    - To filter by score, use 'score:>=[amount]'
    """
    rule34_url = 'https://rule34.xxx/index.php'
 
    @commands.command(name='rule34', aliases=['r34'], brief='Seach images from rule34.xxx', description=rule34_desc)
    async def rule34(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await xml_api.show_post(ctx, tags, score, self.rule34_url)

    xbooru_desc = """
    Searches images from xbooru.com
    
    - For search terms, see https://xbooru.com/index.php?page=help&topic=cheatsheet
    - To filter by score, use 'score:>=[amount]'
    """
    xbooru_url = 'https://xbooru.com/index.php'

    @commands.command(name='xbooru', brief='Seach images from xbooru.com', description=xbooru_desc)
    async def xbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await xml_api.show_post(ctx, tags, score, self.xbooru_url)

    gelbooru_desc = """
    Searches images from gelbooru.com

    - For search terms, see https://gelbooru.com/index.php?page=help&topic=cheatsheet
    - To filter by score, use 'score:>=[amount]'
    """
    gelbooru_url = 'https://gelbooru.com/index.php'

    @commands.command(name='gelbooru', brief='Seach images from gelbooru.com', description=gelbooru_desc)
    async def gelbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await xml_api.show_post(ctx, tags, score, self.gelbooru_url)

    async def cog_before_invoke(self, ctx):
        if 'loli' in ctx.kwargs.get('tags'):
            raise CommandError('No loli allowed')

    def cog_check(self, ctx):
        ch = ctx.channel
        if not ctx.guild or (isinstance(ch, TextChannel) and ch.is_nsfw()):
            return True

        raise NSFWChannelRequired(ch)
