from abc import ABC, abstractmethod

from discord import Embed, Color
from dateutil import parser

import util

from db.model import Post as DBPost


class AbstractPostData(ABC):
    tags: str = None

    @abstractmethod
    def to_content(self) -> dict:
        pass

    @abstractmethod
    def to_embed(self) -> Embed:
        pass

    def has_disallowed_tags(self):
        return util.contains_disallowed_tags(self.tags)

    @classmethod
    @abstractmethod
    def from_db_post(cls, db_post: DBPost):
        pass

    @abstractmethod
    def to_db_post(self) -> DBPost:
        pass


class PostData(AbstractPostData):
    created_at = None
    file_ext = None
    file_url = None
    score = None
    source = None
    tags = None

    def __init__(self, **kwargs):
        self.created_at = kwargs.get('created_at')
        self.file_ext = kwargs.get('file_ext')
        self.file_url = kwargs.get('file_url')
        self.score = kwargs.get('score')
        self.source = kwargs.get('source')
        self.tags = kwargs.get('tags') or kwargs.get('tag_string')

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

    @classmethod
    def from_db_post(cls, db_post: DBPost):
        return cls(**db_post.__dict__)

    def to_db_post(self) -> DBPost:
        db_post = DBPost()
        db_post.file_url = self.file_url
        db_post.file_ext = self.file_ext
        db_post.score = self.score
        db_post.source = self.source

        return db_post


class PostError(AbstractPostData):
    """
    Post used to indicate something went wrong
    """
    def __init__(self, message: str):
        self.message = message

    def to_content(self) -> dict:
        embed = Embed()
        embed.title = 'Error'
        embed.description = self.message

        embed.colour = Color.red()

        return {'content': None, 'embed': embed}
