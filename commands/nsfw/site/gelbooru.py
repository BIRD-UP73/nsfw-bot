from commands.nsfw.site.nsfw_command import NsfwCommand
from url.urls import Gelbooru


class GelbooruCommand(NsfwCommand):
    name = 'gelbooru'
    url = Gelbooru
    max_posts = 20000
