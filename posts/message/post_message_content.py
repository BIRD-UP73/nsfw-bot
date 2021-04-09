from typing import Dict, Union, Optional

from discord import Embed
from discord.embeds import EmptyEmbed


class PostMessageContent:
    embed = None

    def __init__(self, is_animated: bool = False, content: Optional[str] = None, embed: Embed = None):
        self.is_animated: bool = is_animated
        self.content: str = content
        self.embed = embed

    def to_dict(self) -> Dict[str, Union[str, Embed]]:
        if self.is_animated:
            return dict(content=self.content, embed=None)

        return dict(content=None, embed=self.embed)

    def set_footer(self, *, text: str = EmptyEmbed, icon_url: str = EmptyEmbed):
        if self.embed:
            self.embed.set_footer(text=text, icon_url=icon_url)
