from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import Rule34


class Rule34Command(NsfwCommand):
    url = Rule34
    name = 'rule34'
    aliases = ['r34']
    default_tags = 'all'
    max_posts = 200000
