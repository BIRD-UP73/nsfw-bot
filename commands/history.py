from discord.ext.commands import Context, is_nsfw

from commands.nsfw.nsfw_command import NSFWCommand
from posts.post_history import PostHistory
from posts.post_message.history_message import HistoryMessage


class History(NSFWCommand):
    name = 'history'
    aliases = ['hist']
    brief = 'Shows post history'
    check_tags = False

    @is_nsfw()
    async def func(self, ctx: Context):
        channel_hist = PostHistory().hist(ctx.channel)

        if not channel_hist:
            return await ctx.send('No history')

        await HistoryMessage(ctx, channel_hist, self.emojis).create_message()
