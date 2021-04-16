from typing import List, Optional

from discord.ext.commands import Command, Context, is_nsfw, UserInputError

from commands.nsfw.command_options import CommandOptions
from posts.post_message.factory.post_message_factory import PostMessageFactory
from url.urls import URL
from util import tag_util

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
{cheatsheet_text}
"""


async def check_disallowed_tags(ctx: Context):
    tags = ctx.kwargs.get('tags')
    disallowed_tags = tag_util.get_disallowed_tags(tags)

    if len(disallowed_tags) > 0:
        tag_txt = ', '.join(disallowed_tags)
        raise UserInputError(f'You are not allowed to search for: {tag_txt}')


class NSFWCommand(Command):
    name: str = None
    url: URL = None
    emojis: List[str] = default_emojis
    brief = None
    max_posts: int = None
    default_score: int = 50
    aliases: List[str] = []
    check_tags = True

    def __init__(self):
        super(NSFWCommand, self).__init__(self.func, name=self.name, aliases=self.aliases, brief=self.brief)
        if self.url:
            self.brief: str = f'Fetches posts from {self.url.short_url}'

        self.description = create_description(self.url, self.emojis)
        if self.check_tags:
            self.before_invoke(check_disallowed_tags)

    @is_nsfw()
    async def func(self, ctx: Context, score: Optional[int] = default_score, *, tags: str = ''):
        await PostMessageFactory.create_post(ctx, self.command_options(), tags, score)

    def command_options(self) -> CommandOptions:
        return CommandOptions(self.url, self.emojis, self.max_posts)


def create_description(url: URL, emojis: List[str]):
    emoji_txt = '\n'.join(emoji_explanation(emoji) for emoji in emojis)

    cheatsheet_text = ''

    if url:
        cheatsheet_text = f'For search terms, see {url.cheatsheet_url}'

    return description.format(emojis_text=emoji_txt, cheatsheet_text=cheatsheet_text)


def emoji_explanation(emoji: str):
    return f'{emoji} - {emoji_explanations.get(emoji)}'
