from posts.data.post_data import Post
from posts.post_message.post_message_content import MessageContent
from url.urls import URL
from util import tag_util


class JsonPost(Post):
    def __init__(self, board_url: URL, **kwargs):
        super().__init__(board_url, **kwargs)
        self.artist_tag: str = kwargs.get('tag_string_artist')
        self.character_tag: str = kwargs.get('tag_string_character')
        self.copyright_tag: str = kwargs.get('tag_string_copyright')

    def to_message_content(self) -> MessageContent:
        message_content = super().to_message_content()

        if message_content.is_animated:
            return message_content

        if tag_util.is_valid_field_text(self.artist_tag):
            message_content.embed.add_field(name='Artist', value=self.artist_tag)
        if tag_util.is_valid_field_text(self.character_tag):
            message_content.embed.add_field(name='Characters', value=self.character_tag)
        if tag_util.is_valid_field_text(self.copyright_tag):
            message_content.embed.add_field(name='Copyright', value=self.copyright_tag)

        return message_content
