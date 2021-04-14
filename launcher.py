import configparser
import logging
import sys

from discord.ext import commands

from commands.cogs.listeners import Listeners
from commands.cogs.posts_cog import PostCog
from commands.favorites import favorites
from commands.github import github
from commands.help import CustomHelpCommand
from commands.history import post_history
from commands.latency import latency

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('DEFAULT'))

token = details_dict.get('token')
prefix = details_dict.get('prefix')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logging.getLogger()

bot = commands.Bot(
    case_insensitive=True,
    command_prefix=prefix,
    help_command=CustomHelpCommand()
)

bot.add_cog(PostCog())
bot.add_cog(Listeners(bot))

bot.add_command(github)
bot.add_command(latency)
bot.add_command(favorites)
bot.add_command(post_history)

bot.load_extension('commands.nsfw_command')

if __name__ == "__main__":
    bot.run(token)
