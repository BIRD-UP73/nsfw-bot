from discord.ext import commands

from commands.danbooru import danbooru
from commands.github import github
from commands.help import CustomHelpCommand

import configparser

from commands.post_hist import PostHist
from commands.xml_post_cog import XmlPosts

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('DEFAULT'))

token = details_dict.get('token')
prefix = details_dict.get('prefix') or '!'


bot = commands.Bot(
    case_insensitive=True,
    command_prefix=prefix,
    help_command=CustomHelpCommand()
)

bot.add_cog(XmlPosts())
bot.add_cog(PostHist())

bot.add_command(danbooru)
bot.add_command(github)


async def on_ready():
    print(f'{bot.user} is ready')

bot.add_listener(on_ready)

if __name__ == "__main__":
    bot.run(token)
