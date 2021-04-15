from commands.nsfw.nsfw_command import NSFWCommand
from url.urls import URL


class Rule34Command(NSFWCommand):
    url = URL.RULE34
    name = 'rule34'
    aliases = ['r34']
