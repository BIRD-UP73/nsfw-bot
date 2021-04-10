from typing import Callable

from discord.ext.commands import Command

from util.url_util import short_urls, cheat_sheet_url

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


def nsfw_command(**attrs):
    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return create_nsfw_command(func, **attrs)

    return decorator


def create_nsfw_command(func: Callable, **attrs):
    name = attrs.get('name')
    short_url = short_urls.get(name)

    attrs.setdefault('brief', f'Fetches posts from {short_url}')

    emojis = attrs.get('emojis', default_emojis) + attrs.get('extra_emojis', [])

    if emojis:
        emoji_txt = '\n'.join(f'{emoji} - {emoji_explanations.get(emoji)}' for emoji in emojis)
        desc = description.format(emojis_text=emoji_txt, cheatsheet_url=cheat_sheet_url(name))

        attrs.setdefault('description', desc)

    return Command(func, **attrs)
