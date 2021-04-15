from commands.nsfw.nsfw_command import NSFWCommand
from url.urls import URL


class GelbooruCommand(NSFWCommand):
    name = 'gelbooru'
    url = URL.GELBOORU
    max_posts = 20000
