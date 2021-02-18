from discord import Embed
from discord.ext.commands import HelpCommand, Command


class CustomHelpCommand(HelpCommand):
    async def send_command_help(self, command: Command):
        embed = Embed()
        embed.title = command.name
        embed.description = command.brief

        if command.aliases:
            embed.add_field(name='Aliases', value=', '.join(command.aliases), inline=False)

        if command.description:
            embed.add_field(name='Description', value=command.description)

        dest = super().get_destination()
        await dest.send(embed=embed)

    async def send_bot_help(self, mapping: dict):
        embed = Embed()
        embed.title = 'Help'
        embed.description = '**Note:** Commands can only be used in NSFW channels'

        for commands in mapping.values():
            for cmd in commands:
                if cmd.name != 'help':
                    embed.add_field(name=self.get_signature(cmd), value=cmd.brief, inline=False)

        dest = super().get_destination()
        await dest.send(embed=embed)

    def get_signature(self, cmd: Command):
        prefix = super().clean_prefix

        if cmd.signature:
            return f'`{prefix}{cmd.name} {cmd.signature}`'

        return f'`{prefix}{cmd.name}`'
