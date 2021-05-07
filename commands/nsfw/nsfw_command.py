from typing import List, Optional

from discord.ext.commands import Command, Context, is_nsfw, UserInputError

from posts.fetcher.post_fetcher import PostFetcher
from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.paginator.paginator import Paginator
from posts.post_message.post_message import PostMessage
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
    tags = ctx.kwargs.get('tags') or ''

    disallowed_tags = tag_util.get_disallowed_tags(tags)

    if len(disallowed_tags) > 0:
        tag_txt = ', '.join(disallowed_tags)
        raise UserInputError(f'You are not allowed to search for: {tag_txt}')


class NsfwCommand(Command):
    name: str = None
    url: Optional[URL] = None
    emojis: List[str] = default_emojis
    brief = None
    max_posts: int = None
    default_score: int = 50
    default_tags: str = None
    aliases: List[str] = []
    check_tags = True

    def __init__(self):
        super(NsfwCommand, self).__init__(self.func, name=self.name, aliases=self.aliases, brief=self.brief)
        self.description: str = create_description(self.url, self.emojis)

        if self.url:
            self.brief: str = f'Fetches posts from {self.url.short_url}'

        if self.check_tags:
            self.before_invoke(check_disallowed_tags)

    @is_nsfw()
    async def func(self, ctx: Context, score: Optional[int], *, tags: str = None):
        score = score or self.default_score
        tags = tags or self.default_tags

        parsed_tags = self.parsed_tags(tags, score)
        fetcher = self.fetcher(parsed_tags, score)

        await PostMessage(fetcher, ctx, self.emojis).create_message()

    @staticmethod
    def paginator():
        return Paginator()

    def fetcher(self, parsed_tags: str, score: int) -> PostFetcher:
        return XmlPostFetcher(self.url, parsed_tags, score, self.paginator(), self.max_posts)

    def parsed_tags(self, tags: str, score: int) -> str:
        if 'score' not in tags:
            return f'{tags} score:>={score}'

        return tags


def create_description(url: Optional[URL], emojis: List[str]):
    emoji_txt = '\n'.join(emoji_explanation(emoji) for emoji in emojis)

    cheatsheet_text = ''

    if url:
        cheatsheet_text = f'\nFor search terms, see {url.cheatsheet_url}'

    return description.format(emojis_text=emoji_txt, cheatsheet_text=cheatsheet_text)


def emoji_explanation(emoji: str):
    return f'{emoji} - {emoji_explanations.get(emoji)}'
