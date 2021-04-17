from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import Tbib


class TbibCommand(NsfwCommand):
    name = 'tbib'
    aliases = ['thebigimageboard']
    url = Tbib
    default_score = 0
