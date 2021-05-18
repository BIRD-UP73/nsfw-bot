from typing import Union

from discord import DMChannel
from discord.abc import GuildChannel

from posts.data.post_data import Post


class HistoryEvent:
    def __init__(self, post: Post, source: Union[DMChannel, GuildChannel]):
        self.post: Post = post
        self.source: Union[DMChannel, GuildChannel] = source
