from discord.ext.commands import UserInputError

from commands.nsfw.site.nsfw_command import NsfwCommand
from posts.fetcher.json_post_fetcher import JsonPostFetcher
from posts.fetcher.post_fetcher import PostFetcher
from posts.paginator.json_post_paginator import JsonPostPaginator
from url.urls import Danbooru


class DanbooruCommand(NsfwCommand):
    name = 'danbooru'
    url = Danbooru
    aliases = ['dbooru']

    @staticmethod
    def paginator():
        return JsonPostPaginator()

    def fetcher(self, parsed_tags: str, score: int) -> PostFetcher:
        return JsonPostFetcher(self.url(), parsed_tags, self.paginator())

    def parsed_tags(self, tags: str, score: int) -> str:
        split_tags = tags.split(' ')

        if len(split_tags) > 2:
            raise UserInputError(f'Cannot search for more than 2 tags. You entered {len(split_tags)}.')
        if len(split_tags) == 2:
            return tags
        return super().parsed_tags(tags, score)
