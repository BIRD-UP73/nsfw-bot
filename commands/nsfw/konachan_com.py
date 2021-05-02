from commands.nsfw.nsfw_command import NsfwCommand
from posts.paginator.json_post_paginator import JsonPostPaginator
from url.urls import KonachanCom


class KonachanComCommand(NsfwCommand):
    name = 'konachan'
    url = KonachanCom

    @staticmethod
    def paginator():
        return JsonPostPaginator()
