from discord import Color

from posts.post_message.post_message_content import MessageContent
from url.urls import URL
from util import tag_util


class Post:
    def __init__(self, **kwargs):
        self.board_url: URL = kwargs.get('board_url')
        self.created_at: str = kwargs.get('created_at')
        self.file_ext: str = kwargs.get('file_ext')
        self.file_url: str = kwargs.get('file_url')
        self.score: str = kwargs.get('score')
        self.source: str = kwargs.get('source')
        self.tags: str = kwargs.get('tags') or kwargs.get('tag_string')
        self.post_id: int = int(kwargs.get('id', 0))

    def is_error(self) -> bool:
        return False

    def is_animated(self) -> bool:
        return tag_util.is_video(self.file_ext)

    def to_message_content(self) -> MessageContent:
        return MessageContent(**self.__dict__)

    @classmethod
    def from_dict(cls, **kwargs):
        tags = kwargs.get('tags') or kwargs.get('tag_string')

        if tag_util.has_disallowed_tags(tags):
            disallowed_tags = tag_util.get_disallowed_tags(tags)
            return DisallowedTagsPost(f'Found disallowed tags: {disallowed_tags}')

        return cls(**kwargs)


class ErrorPost(Post):
    """
    Post used to indicate something went wrong
    """
    def __init__(self, message: str):
        super().__init__()
        self.message: str = message

    def is_animated(self) -> bool:
        return False

    def is_error(self) -> bool:
        return True

    def to_message_content(self) -> MessageContent:
        return MessageContent(title='Error', description=self.message, color=Color.red())


class NonExistentPost(ErrorPost):
    def __init__(self):
        super().__init__('Post no longer exists')


class DisallowedTagsPost(ErrorPost):
    default_message = 'Post contains disallowed tags. Please try again.'

    def __init__(self, message=default_message):
        super().__init__(message)
