from collections import deque
from typing import Dict, Deque, Union, List

from discord import DMChannel, TextChannel

from posts.data.post_data import Post
from posts.post_entry import PostEntry
from posts.singleton import Singleton


class PostHistory(metaclass=Singleton):
    history: Dict[int, Deque[PostEntry]] = {}

    def add_to_history(self, channel: Union[DMChannel, TextChannel], post: Post):
        if post.is_error():
            return

        channel_id = channel.id if isinstance(channel, DMChannel) else channel.guild.id

        self.history.setdefault(channel_id, deque(maxlen=25))
        self.history[channel_id].append(PostEntry.from_post_data(post))

    def hist(self, channel: Union[DMChannel, TextChannel]) -> List[PostEntry]:
        channel_id = channel.id if isinstance(channel, DMChannel) else channel.guild.id
        return list(self.history.get(channel_id, []))
