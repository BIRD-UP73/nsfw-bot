from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

import xml_api

desc = """
Searches images from xbooru.com

- For search terms, see https://xbooru.com/index.php?page=help&topic=cheatsheet
- To filter by score, use 'score:>=[amount]'
"""

url = 'https://xbooru.com/index.php'


@is_nsfw()
@commands.command(name='xbooru', brief='Seach images from xbooru.com', description=desc)
async def xbooru(ctx: Context, score: Optional[int] = 50, *, tags: str):
    await xml_api.get_rule_34(ctx, tags, score, url)


@xbooru.error
async def handle_error(ctx: Context, error):
    await ctx.send(error)
