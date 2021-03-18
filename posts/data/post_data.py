from dateutil import parser
from discord import Embed, Color

from posts.message.post_message_content import PostMessageContent
from util import util


class PostData:
    def __init__(self, **kwargs):
        self.created_at: str = kwargs.get('created_at')
        self.file_ext: str = kwargs.get('file_ext')
        self.file_url: str = kwargs.get('file_url')
        self.score: str = kwargs.get('score')
        self.source: str = kwargs.get('source')
        self.tags: str = kwargs.get('tags') or kwargs.get('tag_string')
        self.post_id: int = int(kwargs.get('id') or 0)

    def is_error(self) -> bool:
        return False

    def has_disallowed_tags(self) -> bool:
        return util.contains_disallowed_tags(self.tags)

    def is_animated(self) -> bool:
        return util.is_video(self.file_ext)

    def to_message_content(self) -> PostMessageContent:
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

        return PostMessageContent(self.is_animated(), self.file_url, embed)


class PostError(PostData):
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

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.colour = Color.red()

        embed.title = 'Error'
        embed.add_field(name='Error', value=self.message)

        return embed


class PostNoLongerExists(PostError):
    def __init__(self):
        super().__init__('Post no longer exists')


class PostHasDisallowedTags(PostError):
    def __init__(self):
        super().__init__('Post contains disallowed tags. Please try again.')
