from typing import Dict, Union, Optional

from discord import Embed


class PostMessageContent:
    def __init__(self, is_animated: bool = False, content: Optional[str] = None, embed: Embed = None):
        self.is_animated: bool = is_animated
        self.content: str = content
        self.embed = embed

    def to_dict(self) -> Dict[str, Union[str, Embed]]:
        if self.is_animated:
            return dict(content=self.content, embed=None)

        return dict(content=None, embed=self.embed)
