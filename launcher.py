from discord.ext import commands

from commands.danbooru import danbooru
from commands.gelbooru import gelbooru
from commands.help import CustomHelpCommand
from commands.rule34 import rule34

import configparser

from commands.xbooru import xbooru

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('DEFAULT'))

token = details_dict.get('token')

bot = commands.Bot(
    case_insensitive=True,
    command_prefix='!',
    help_command=CustomHelpCommand()
)

bot.add_command(rule34)
bot.add_command(xbooru)
bot.add_command(gelbooru)
bot.add_command(danbooru)


async def on_ready():
    print(f'{bot.user} is ready')

bot.add_listener(on_ready)

if __name__ == "__main__":
    bot.run(token)
