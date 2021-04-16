from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import URL


class DanbooruCommand(NsfwCommand):
    name = 'danbooru'
    url = URL.DANBOORU
    aliases = ['dbooru']
