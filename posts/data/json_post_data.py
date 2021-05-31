from posts.data.post_data import Post, DisallowedTagsPost
from util import tag_util


class JsonPost(Post):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artist_tag: str = kwargs.get('tag_string_artist')
        self.character_tag: str = kwargs.get('tag_string_character')
        self.copyright_tag: str = kwargs.get('tag_string_copyright')

    @classmethod
    def from_dict(cls, **kwargs):
        tags = kwargs.get('tags') or kwargs.get('tag_string')

        if tag_util.has_disallowed_tags(tags):
            disallowed_tags = tag_util.get_disallowed_tags(tags)
            return DisallowedTagsPost(f'Found disallowed tags: {disallowed_tags}')

        return JsonPost(**kwargs)
