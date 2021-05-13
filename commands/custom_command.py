from typing import List

from discord.ext.commands import Command, Context


class CustomCommand(Command):
    name: str = ''
    brief: str = ''
    description: str = ''
    aliases: List[str] = []

    def __init__(self):
        data = {
            'name': self.name,
            'aliases': self.aliases,
            'brief': self.brief,
            'description': self.description
        }

        super().__init__(self.func, **data)

    def func(self, ctx: Context):
        pass
