from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import URL


class Rule34Command(NsfwCommand):
    url = URL.RULE34
    name = 'rule34'
    aliases = ['r34']
