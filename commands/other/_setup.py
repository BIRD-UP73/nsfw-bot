from discord.ext.commands import Bot

from commands.other.github import Github
from commands.other.latency import Latency


def setup(bot: Bot):
    bot.add_command(Github())
    bot.add_command(Latency())
