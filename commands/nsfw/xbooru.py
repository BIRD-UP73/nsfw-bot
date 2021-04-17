from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import Xbooru


class XbooruCommand(NsfwCommand):
    name = 'xbooru'
    url = Xbooru
