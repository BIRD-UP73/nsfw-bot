from abc import ABC, abstractmethod

from dateutil import parser
from discord import Embed, Color

from util import util


class AbstractPostData(ABC):
    tags: str = None

    @abstractmethod
    def to_content(self) -> dict:
        """
        Converts this post data to a dictionary with arguments that
        are used in `Message.send`

        For example: `{'content': 'Message content', 'embed': <embed data>}

        :return: the dictionary with content
        """
        pass

    def has_disallowed_tags(self):
        """
        Checks if the tags contain disallowed tags
        """
        return util.contains_disallowed_tags(self.tags)


class PostData(AbstractPostData):
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

    def to_content(self) -> dict:
        if not util.is_image(self.file_ext):
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

    def to_content(self) -> dict:
        embed = Embed()
        embed.title = 'Error'
        embed.description = self.message

        embed.colour = Color.red()

        return {'content': None, 'embed': embed}
