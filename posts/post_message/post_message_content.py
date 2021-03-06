from typing import Dict, Union

from discord import Embed


class MessageContent:
    """
    Message content in a :class Post, can contain message text as well as an :class Embed
    """
    def __init__(self, is_animated: bool = False, content: str = None, embed: Embed = None):
        self.is_animated: bool = is_animated
        self.content: str = content
        self.embed = embed

    def to_dict(self) -> Dict[str, Union[str, Embed]]:
        if self.is_animated:
            return dict(content=self.content, embed=None)

        return dict(content=None, embed=self.embed)
