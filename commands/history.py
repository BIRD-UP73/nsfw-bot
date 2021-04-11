from discord.ext.commands import Context, is_nsfw

from commands.nsfw_command import nsfw_command
from posts.post_history import PostHistory
from posts.post_message.history_message import HistoryMessage


@is_nsfw()
@nsfw_command(name='history', brief='Shows post history', aliases=['hist'])
async def post_history(ctx: Context):
    channel_hist = PostHistory().hist(ctx.channel)

    if not channel_hist:
        return await ctx.send('No history')

    await HistoryMessage(ctx, channel_hist).create_message()
