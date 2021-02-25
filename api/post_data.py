from dateutil import parser
from discord import Embed, Color

from util import util


class PostData:
    created_at = None
    file_ext = None
    file_url = None
    score = None
    source = None
    tags = None
    id = 0

    def __init__(self, **kwargs):
        self.created_at = kwargs.get('created_at')
        self.file_ext = kwargs.get('file_ext')
        self.file_url = kwargs.get('file_url')
        self.score = kwargs.get('score')
        self.source = kwargs.get('source')
        self.tags = kwargs.get('tags') or kwargs.get('tag_string')
        self.id = kwargs.get('id')

    def is_error(self):
        return False

    def has_disallowed_tags(self) -> bool:
        return util.contains_disallowed_tags(self.tags)

    def is_animated(self):
        return util.is_video(self.file_ext)

    def to_content(self) -> dict:
        if self.is_animated():
            return {'content': self.file_url, 'embed': None}

        return {'content': None, 'embed': self.to_embed()}

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.colour = Color.green()

        if self.source:
            embed.add_field(name='Source', value=self.source, inline=False)
        if self.created_at:
            embed.timestamp = parser.parse(self.created_at)
        if self.score:
            embed.set_footer(text=f'Score: {self.score}')

        if self.file_url:
            embed.set_image(url=self.file_url)

        return embed


class PostError(PostData):
    """
    Post used to indicate something went wrong
    """
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def is_animated(self):
        return False

    def is_error(self):
        return True

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.colour = Color.red()

        embed.title = 'Error'
        embed.add_field(name='Error', value=self.message)

        return embed
