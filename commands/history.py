from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from posts.post_history import PostHistory
from posts.message.history_message import HistoryMessage

description = """
⭐   add post to your favorites
🗑️  remove message
⬅➡ scroll through pages
"""


@is_nsfw()
@commands.command(name='history', aliases=['hist'], brief='Post history', description=description)
async def post_history(ctx: Context):
    channel_hist = PostHistory().hist(ctx.channel)

    if not channel_hist:
        return await ctx.send('No history')

    await HistoryMessage(ctx, channel_hist).create_message()
