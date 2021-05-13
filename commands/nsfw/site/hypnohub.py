from commands.nsfw.site.nsfw_command import NsfwCommand
from url.urls import Hypnohub


class HypnohubCommand(NsfwCommand):
    name = 'hypnohub'
    aliases = ['hypno']
    url = Hypnohub
    default_score = 0
