from typing import Union

from discord import DMChannel, User
from discord.abc import GuildChannel

from posts.data.post_data import Post


class HistoryEvent:
    def __init__(self, user: User, post: Post, source: Union[DMChannel, GuildChannel]):
        self.user: User = user
        self.post: Post = post
        self.source: Union[DMChannel, GuildChannel] = source
