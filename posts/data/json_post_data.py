from posts.data.post_data import Post
from url.urls import URL


class JsonPost(Post):
    def __init__(self, board_url: URL, **kwargs):
        super().__init__(board_url, **kwargs)
        self.artist_tag: str = kwargs.get('tag_string_artist')
        self.character_tag: str = kwargs.get('tag_string_character')
        self.copyright_tag: str = kwargs.get('tag_string_copyright')
