from typing import Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, NSFWChannelRequired, CommandError

import util
from api import xml_api

short_urls = {
    'rule34': 'rule34.xxx',
    'gelbooru': 'gelbooru.com',
    'xbooru': 'xbooru.com',
    'tbib': 'tbib.org'
}

aliases = {
    'rule34': ['r34']
}


def get_long_url(command_name: str):
    return f'https://{short_urls.get(command_name)}/index.php'


def get_data(command_name: str):
    url = short_urls.get(command_name)
    description = f"""
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

    async def cog_before_invoke(self, ctx):
        if util.contains_disallowed_tags(ctx.kwargs.get('tags')):
            raise CommandError('Post contains disallowed tag')

    def cog_check(self, ctx):
        ch = ctx.channel
        if not ctx.guild or (isinstance(ch, TextChannel) and ch.is_nsfw()):
            return True

        raise NSFWChannelRequired(ch)
