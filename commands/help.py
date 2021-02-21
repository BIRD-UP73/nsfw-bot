from discord import Embed
from discord.ext.commands import HelpCommand, Command


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

    async def send_bot_help(self, mapping: dict):
        embed = Embed()
        embed.title = 'Help'
        embed.description = '**Note:** Commands can only be used in NSFW channels'

        cmd_names = []

        for commands in mapping.values():
            for cmd in commands:
                if cmd.name != 'help' and cmd.name not in cmd_names:
                    embed.add_field(name=self.get_signature(cmd), value=cmd.brief, inline=False)
                    cmd_names.append(cmd.name)

        await self.context.send(embed=embed)

    def get_signature(self, cmd: Command):
        if cmd.signature:
            return f'`{self.clean_prefix}{cmd.name} {cmd.signature}`'

        return f'`{self.clean_prefix}{cmd.name}`'
