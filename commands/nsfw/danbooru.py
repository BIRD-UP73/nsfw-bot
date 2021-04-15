from commands.nsfw.nsfw_command import NSFWCommand
from url.urls import URL


class DanbooruCommand(NSFWCommand):
    name = 'danbooru'
    url = URL.DANBOORU
    aliases = ['dbooru']
