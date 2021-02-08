from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

import api_json

desc = """
Searches images from danbooru.com

- For search terms, see https://danbooru.donmai.us/wiki_pages/help:cheatsheet
- To filter by score, use 'score:>=[amount]'
"""


@is_nsfw()
@commands.command(name='danbooru', aliases=['dbooru'], brief='Seach images from danbooru.com', description=desc)
async def danbooru(ctx: Context, score: Optional[int] = 50, *, tags: str, ):
    embed = api_json.get_posts(tags, score)

    if not embed:
        return await ctx.send('No images found')

    await ctx.send(embed=embed)
