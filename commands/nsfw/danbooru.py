from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import Danbooru


class DanbooruCommand(NsfwCommand):
    name = 'danbooru'
    url = Danbooru
    aliases = ['dbooru']
