from discord import Embed

from posts.data.post_data import PostData
from util import util


class JsonPostData(PostData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artist_tag: str = kwargs.get('tag_string_artist')
        self.character_tag: str = kwargs.get('tag_string_character')
        self.copyright_tag: str = kwargs.get('tag_string_copyright')

    def to_embed(self) -> Embed:
        embed = super().to_embed()

        if util.is_valid_field_text(self.artist_tag):
            embed.add_field(name='Artist', value=self.artist_tag)
        if util.is_valid_field_text(self.character_tag):
            embed.add_field(name='Characters', value=self.character_tag)
        if util.is_valid_field_text(self.copyright_tag):
            embed.add_field(name='Copyright', value=self.copyright_tag)

        return embed
