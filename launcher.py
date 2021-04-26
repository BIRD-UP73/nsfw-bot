import configparser
import logging
import sys

from discord.ext import commands

from commands.favorites import Favorites
from commands.github import github
from commands.help import CustomHelpCommand
from commands.history import History
from commands.latency import latency
from commands.nsfw.listeners import Listeners

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('DEFAULT'))

token = details_dict.get('token')
prefix = details_dict.get('prefix')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

bot = commands.Bot(
    case_insensitive=True,
    command_prefix=prefix,
    help_command=CustomHelpCommand(),
)

bot.add_cog(Listeners(bot))

bot.add_command(github)
bot.add_command(latency)
bot.add_command(Favorites())
bot.add_command(History())

bot.load_extension('commands.nsfw._setup')

if __name__ == "__main__":
    bot.run(token)
