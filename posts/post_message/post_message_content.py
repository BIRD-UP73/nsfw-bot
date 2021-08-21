from datetime import datetime
from typing import Dict, Union, List, Optional

from dateutil import parser
from discord import Embed, Color

from util import tag_util


class MessageField:
    def __init__(self, name: str, value: str, inline: bool = False):
        self.name: str = name
        self.value: str = value
        self.inline: bool = inline

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'inline': self.inline
        }


class MessageContent:
    """
    Message content in a :class Post, can contain message text as well as an :class Embed
    """

    page: int = 0
    total_pages: int = 0
    default_color: Color = Color.green()
    default_time = datetime.now()

    def __init__(self, **kwargs):
        self.score: int = kwargs.get('score', 0)
        self.title: str = kwargs.get('title')
        self.description: str = kwargs.get('description')
        self.file_url: str = kwargs.get('file_url')
        self.file_ext: str = kwargs.get('file_ext')
        self.timestamp: Union[str, datetime] = kwargs.get('timestamp', kwargs.get('created_at', self.default_time))
        self.source: str = kwargs.get('source')
        self.artist_tag: str = kwargs.get('artist_tag')
        self.character_tag: str = kwargs.get('character_tag')
        self.copyright_tag: str = kwargs.get('copyright_tag')
        self.color: Color = kwargs.get('color', self.default_color)
        self.embed_fields: List[MessageField] = kwargs.get('fields', [])

    def to_dict(self) -> Dict[str, Union[str, Embed]]:
        return dict(content=self.to_content(), embed=self.to_embed())

    def add_field(self, name: str, value: str, inline: bool = False):
        self.embed_fields.append(MessageField(name, value, inline))

    def to_content(self) -> str:
        content_lines = [self.page_counter()]

        if self.file_url:
            content_lines.append(self.file_url)

        return '\n'.join(content_lines)

    def to_embed(self) -> Optional[Embed]:
        if self.is_video():
            return None

        embed = Embed(title=self.title, color=self.color, description=self.description)

        if self.file_url:
            embed.set_image(url=self.file_url)

        if self.source:
            embed.add_field(name='Source', value=self.source, inline=False)
        if tag_util.is_valid_field_text(self.artist_tag):
            embed.add_field(name='Artist', value=self.artist_tag)
        if tag_util.is_valid_field_text(self.character_tag):
            embed.add_field(name='Characters', value=self.character_tag)
        if tag_util.is_valid_field_text(self.copyright_tag):
            embed.add_field(name='Copyright', value=self.copyright_tag)

        footer_elements = [self.page_counter()]
        if self.score:
            footer_elements.append(f'Score: {self.score}')

        embed.set_footer(text=' • '.join(footer_elements))

        if self.timestamp:
            embed.timestamp = self.parse_timestamp()

        for field in self.embed_fields:
            embed.add_field(**field.to_dict())

        return embed

    def is_video(self):
        if not self.file_ext:
            return False

        return tag_util.is_video(self.file_ext)

    def page_counter(self):
        return f'Page {self.page} of {self.total_pages}'

    def parse_timestamp(self):
        if isinstance(self.timestamp, datetime):
            return self.timestamp

        if self.timestamp.isnumeric():
            return datetime.fromtimestamp(int(self.timestamp))

        return parser.parse(self.timestamp)
