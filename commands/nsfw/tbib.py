from commands.nsfw.nsfw_command import NSFWCommand
from url.urls import URL


class TbibCommand(NSFWCommand):
    name = 'tbib'
    url = URL.TBIB
    default_score = 0
