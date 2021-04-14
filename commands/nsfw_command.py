from typing import Callable

from discord.ext.commands import Command

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
    """
    TODO: Things to add
    - Emojis
    - URL
    -
    """
    def __init__(self, url: URL, func, **kwargs):
        super(NSFWCommand, self).__init__(func, **kwargs)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        if not self._description:
            self._description = value


# def create_nsfw_command(func: Callable, **attrs):
#     name = attrs.get('name')
#     short_url = short_urls.get(name)
#
#     attrs.setdefault('brief', f'Fetches posts from {short_url}')
#
#     emojis = attrs.get('emojis', default_emojis) + attrs.get('extra_emojis', [])
#
#     if emojis:
#         emoji_txt = '\n'.join(f'{emoji} - {emoji_explanations.get(emoji)}' for emoji in emojis)
#         desc = description.format(emojis_text=emoji_txt, cheatsheet_url=cheat_sheet_url(name))
#
#         attrs.setdefault('description', desc)
#
#     return Command(func, **attrs)
