from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import URL


class GelbooruCommand(NsfwCommand):
    name = 'gelbooru'
    url = URL.GELBOORU
    max_posts = 20000
