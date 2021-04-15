from typing import List, Optional

from discord.ext.commands import Command, Context, is_nsfw

from posts.post_message.factory.post_message_factory import PostMessageFactory
from url.urls import URL

default_emojis = ['⭐', '⬅', '➡', '🔁', '🗑️']

emoji_explanations = {
    '⭐': 'add post to your favorites',
    '🗑️': 'removes the current message',
    '🔁': 'fetches a random post',
    '➡': 'fetches the next post',
    '⬅': 'fetches the previous post',
    '⛔': 'removes a favorite'
}

description = """
**Emojis**
{emojis_text}

For search terms, see {cheatsheet_url}
"""


class NSFWCommand(Command):
    name: str = None
    emojis: List[str] = default_emojis
    url: URL = None
    max_posts: int = None
    default_score: int = 50
    aliases = []

    def __init__(self):
        super(NSFWCommand, self).__init__(self.func, name=self.name, aliases=self.aliases)
        self.brief = f'Fetches posts from {self.url.short_url}'
        self.description = create_description(self.url, self.emojis)

    @is_nsfw()
    async def func(self, ctx: Context, score: Optional[int] = default_score, *, tags: str = ''):
        await PostMessageFactory.create_post(ctx, self.url, tags, score, self.max_posts)


def create_description(url: URL, emojis: List[str]):
    emoji_txt = '\n'.join(emoji_explanation(emoji) for emoji in emojis)
    return description.format(emojis_text=emoji_txt, cheatsheet_url=url.cheatsheet_url)


def emoji_explanation(emoji: str):
    return f'{emoji} - {emoji_explanations.get(emoji)}'
