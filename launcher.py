import configparser

from discord.ext import commands

from commands.cogs.listeners import Listeners
from commands.cogs.posts_cog import PostCog
from commands.favorites import Favorites
from commands.github import github
from commands.help import CustomHelpCommand
from commands.history import PostHist
from commands.latency import latency

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('DEFAULT'))

token = details_dict.get('token')
prefix = details_dict.get('prefix')


bot = commands.Bot(
    case_insensitive=True,
    command_prefix=prefix,
    help_command=CustomHelpCommand()
)

bot.add_cog(PostCog())
bot.add_cog(PostHist())
bot.add_cog(Listeners(bot))
bot.add_cog(Favorites())

bot.add_command(github)
bot.add_command(latency)

if __name__ == "__main__":
    bot.run(token)
