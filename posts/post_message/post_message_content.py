from datetime import datetime
from typing import Dict, Union

from dateutil import parser
from discord import Embed, Color

from util import tag_util


class MessageContent:
    """
    Message content in a :class Post, can contain message text as well as an :class Embed
    """

    page: int = 0
    total_pages: int = 0
    default_color: Color = Color.green()

    def __init__(self, **kwargs):
        self.score: int = kwargs.get('score', 0)
        self.title: str = kwargs.get('title')
        self.description: str = kwargs.get('description')
        self.file_url: str = kwargs.get('file_url')
        self.file_ext: str = kwargs.get('file_ext')
        self.timestamp: str = kwargs.get('timestamp') or kwargs.get('created_at') or datetime.now()
        self.source: str = kwargs.get('source')
        self.artist_tag: str = kwargs.get('artist_tag')
        self.character_tag: str = kwargs.get('character_tag')
        self.copyright_tag: str = kwargs.get('copyright_tag')
        self.color: Color = kwargs.get('color', self.default_color)

    def to_dict(self) -> Dict[str, Union[str, Embed]]:
        if tag_util.is_video(self.file_ext):
            return dict(content=self.to_content(), embed=None)

        return dict(content=None, embed=self.to_embed())

    def to_content(self) -> str:
        content_lines = [self.page_counter(), self.file_url]
        return '\n'.join(content_lines)

    def to_embed(self) -> Embed:
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

        return embed

    def page_counter(self):
        return f'Page {self.page} of {self.total_pages}'

    def parse_timestamp(self):
        if self.timestamp.isnumeric():
            return datetime.fromtimestamp(int(self.timestamp))

        return parser.parse(self.timestamp)
