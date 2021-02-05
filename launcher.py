from discord import Intents
from discord.ext import commands

import configparser

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('DEFAULT'))

token = details_dict.get('token')

bot = commands.Bot(
    case_insensitive=True,
    command_prefix='!'
)


async def on_ready():
    print(f'{bot.user} is ready')

bot.add_listener(on_ready)

if __name__ == "__main__":
    # bot.run(token)
    print('run')
