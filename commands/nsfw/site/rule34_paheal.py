from commands.nsfw.site.nsfw_command import NsfwCommand
from posts.paginator.json_post_paginator import JsonPostPaginator
from url.urls import Rule34Paheal


class Rule34PahealCommand(NsfwCommand):
    name = 'paheal'
    url = Rule34Paheal
    default_score = 0

    @staticmethod
    def paginator():
        return JsonPostPaginator()
