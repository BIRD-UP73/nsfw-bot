from discord.ext.commands import Bot

from commands.nsfw.site.danbooru import DanbooruCommand
from commands.nsfw.site.gelbooru import GelbooruCommand
from commands.nsfw.site.hypnohub import HypnohubCommand
from commands.nsfw.site.konachan_com import KonachanComCommand
from commands.nsfw.site.rule34_paheal import Rule34PahealCommand
from commands.nsfw.site.rule_34 import Rule34Command
from commands.nsfw.site.tbib import TbibCommand
from commands.nsfw.site.xbooru import XbooruCommand


def setup(bot: Bot):
    bot.add_command(DanbooruCommand())
    bot.add_command(GelbooruCommand())
    bot.add_command(HypnohubCommand())
    bot.add_command(KonachanComCommand())
    bot.add_command(Rule34Command())
    bot.add_command(Rule34PahealCommand())
    bot.add_command(TbibCommand())
    bot.add_command(XbooruCommand())
