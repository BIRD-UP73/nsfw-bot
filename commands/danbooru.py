from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, is_nsfw, CommandError

from api import api_json

desc = """
Searches images from danbooru.com

- For search terms, see https://danbooru.donmai.us/wiki_pages/help:cheatsheet
- To filter by score, use 'score:>=[amount]'
"""


@is_nsfw()
@commands.command(name='danbooru', aliases=['dbooru'], brief='Seach images from danbooru.com', description=desc)
async def danbooru(ctx: Context, score: Optional[int] = 50, *, tags: str, ):
    if 'loli' in tags:
        raise CommandError('No loli allowed')

    await api_json.show_post(ctx, tags, score)


@danbooru.error
async def on_error(ctx: Context, error):
    await ctx.send(error)
    raise error
