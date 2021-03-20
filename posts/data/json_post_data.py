from posts.data.post_data import PostData
from posts.message.post_message_content import PostMessageContent
from util import util


class JsonPostData(PostData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artist_tag: str = kwargs.get('tag_string_artist')
        self.character_tag: str = kwargs.get('tag_string_character')
        self.copyright_tag: str = kwargs.get('tag_string_copyright')

    def to_message_content(self) -> PostMessageContent:
        message_content = super().to_message_content()

        if message_content.is_animated:
            return message_content

        if util.is_valid_field_text(self.artist_tag):
            message_content.embed.add_field(name='Artist', value=self.artist_tag)
        if util.is_valid_field_text(self.character_tag):
            message_content.embed.add_field(name='Characters', value=self.character_tag)
        if util.is_valid_field_text(self.copyright_tag):
            message_content.embed.add_field(name='Copyright', value=self.copyright_tag)

        return message_content
