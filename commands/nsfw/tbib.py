from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import URL


class TbibCommand(NsfwCommand):
    name = 'tbib'
    aliases = ['thebigimageboard']
    url = URL.TBIB
    default_score = 0
