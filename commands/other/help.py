import itertools
from typing import Mapping, Optional, List

from discord import Embed
from discord.ext.commands import HelpCommand, Command, Cog


class CustomHelpCommand(HelpCommand):
    async def send_command_help(self, command: Command):
        embed = Embed()
        embed.title = command.name
        embed.description = command.brief

        if command.description:
            embed.add_field(name='Description', value=command.description)

        if command.aliases:
            embed.add_field(name='Aliases', value=', '.join(command.aliases), inline=False)

        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]]):
        embed = Embed()
        embed.title = 'Help'
        embed.description = '**Note:** Commands can only be used in NSFW channels'

        unique_commands = {cmd.name: cmd for cmd in itertools.chain.from_iterable(mapping.values())}
        del unique_commands['help']

        for cmd in unique_commands.values():
            embed.add_field(name=self.full_signature(cmd), value=cmd.brief, inline=False)

        await self.context.send(embed=embed)

    def full_signature(self, cmd: Command):
        if cmd.signature:
            return f'`{self.clean_prefix}{cmd.name} {cmd.signature}`'

        return f'`{self.clean_prefix}{cmd.name}`'
