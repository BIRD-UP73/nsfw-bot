from discord.ext.commands import UserInputError

from commands.nsfw.nsfw_command import NsfwCommand
from url.urls import Danbooru


class DanbooruCommand(NsfwCommand):
    name = 'danbooru'
    url = Danbooru
    aliases = ['dbooru']

    @staticmethod
    def parsed_tags(tags: str, score: int) -> str:
        split_tags = tags.split(' ')

        if len(split_tags) > 2:
            raise UserInputError(f'Cannot search for more than 2 tags. You entered {len(split_tags)}.')
        if len(split_tags) == 2:
            return tags
        return super().parsed_tags(tags, score)
