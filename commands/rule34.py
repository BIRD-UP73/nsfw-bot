from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

import xml_api

desc = """
Searches images from rule34.xxx

- For search terms, see https://rule34.xxx/index.php?page=help&topic=cheatsheet
- To filter by score, use 'score:>=[amount]'
"""

url = 'https://rule34.xxx/index.php'


@is_nsfw()
@commands.command(name='rule34', aliases=['r34'], brief='Seach images from rule34.xxx', description=desc)
async def rule34(ctx: Context, score: Optional[int] = 50, *, tags: str):
    await xml_api.get_rule_34(ctx, tags, score, url)
