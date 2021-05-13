from discord.ext.commands import Bot

from commands.nsfw.favorites import Favorites
from commands.nsfw.history import History


def setup(bot: Bot):
    bot.add_command(Favorites())
    bot.add_command(History())
