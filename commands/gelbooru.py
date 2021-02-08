from typing import Optional

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

import xml_api
from urls import SiteType

desc = """
Searches images from gelbooru.com

- For search terms, see https://gelbooru.com/index.php?page=help&topic=cheatsheet
- To filter by score, use 'score:>=[amount]'
"""

url = 'https://gelbooru.com/index.php'


@is_nsfw()
@commands.command(name='gelbooru', brief='Seach images from gelbooru.com', description=desc)
async def gelbooru(ctx: Context, score: Optional[int] = 50, *, tags: str):
    await xml_api.get_rule_34(ctx, tags, score, url)


@gelbooru.error
async def handle_error(ctx: Context, error):
    await ctx.send(error)
