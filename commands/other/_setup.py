from discord.ext.commands import Bot

from commands.other.github import Github
from commands.other.latency import Latency
from commands.other.listeners import Listeners


def setup(bot: Bot):
    bot.add_command(Github())
    bot.add_command(Latency())
    bot.add_cog(Listeners(bot))
