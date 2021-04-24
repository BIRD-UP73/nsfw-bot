from discord.ext.commands import Bot

from commands.nsfw.danbooru import DanbooruCommand
from commands.nsfw.gelbooru import GelbooruCommand
from commands.nsfw.hypnohub import HypnohubCommand
from commands.nsfw.konachan_com import KonachanComCommand
from commands.nsfw.rule34_paheal import Rule34PahealCommand
from commands.nsfw.rule_34 import Rule34Command
from commands.nsfw.tbib import TbibCommand
from commands.nsfw.xbooru import XbooruCommand


def setup(bot: Bot):
    bot.add_command(DanbooruCommand())
    bot.add_command(GelbooruCommand())
    bot.add_command(HypnohubCommand())
    bot.add_command(KonachanComCommand())
    bot.add_command(Rule34Command())
    bot.add_command(Rule34PahealCommand())
    bot.add_command(TbibCommand())
    bot.add_command(XbooruCommand())
