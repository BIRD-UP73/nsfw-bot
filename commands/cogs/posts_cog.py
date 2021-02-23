from typing import Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, NSFWChannelRequired, CommandError

from util import util
from util.url_util import short_urls, get_long_url
from api import xml_api, json_api


aliases = {
    'rule34': ['r34'],
    'danbooru': ['dbooru']
}

desc = {
    'danbooru': """
    Searches images from danbooru.com
    
    - For search terms, see https://danbooru.donmai.us/wiki_pages/help:cheatsheet
    - To filter by score, use 'score:>=[amount]'
    """
}


def get_data(command_name: str):
    url = short_urls.get(command_name)
    description = desc.get(command_name) or f"""
                Searches images from {url}

                - For search terms, see https://{url}/index.php?page=help&topic=cheatsheet
                - To filter by score, use 'score:>=[amount]'
                """

    data_dict = dict(
        name=command_name,
        brief=f'Search images from {url}',
        description=description,
    )

    if command_name in aliases:
        data_dict['aliases'] = aliases.get(command_name)

    return data_dict


class XmlPosts(commands.Cog):
    @commands.command(**get_data('rule34'))
    async def rule34(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await xml_api.show_post(ctx, tags, score, get_long_url(ctx.command.name))

    @commands.command(**get_data('xbooru'))
    async def xbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await xml_api.show_post(ctx, tags, score, get_long_url(ctx.command.name))

    @commands.command(**get_data('gelbooru'))
    async def gelbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await xml_api.show_post(ctx, tags, score, get_long_url(ctx.command.name))

    @commands.command(**get_data('tbib'))
    async def tbib(self, ctx: Context, *, tags: str):
        await xml_api.show_post(ctx, tags, 0, get_long_url(ctx.command.name), skip_score=True)

    @commands.command(**get_data('danbooru'))
    async def danbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str, ):
        await json_api.show_post(ctx, tags, score)

    async def cog_before_invoke(self, ctx):
        if util.contains_disallowed_tags(ctx.kwargs.get('tags')):
            raise CommandError('Post contains disallowed tag')

    def cog_check(self, ctx):
        ch = ctx.channel
        if not ctx.guild or (isinstance(ch, TextChannel) and ch.is_nsfw()):
            return True

        raise NSFWChannelRequired(ch)
