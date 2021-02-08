from discord import Embed
from discord.ext.commands import HelpCommand, Command


class CustomHelpCommand(HelpCommand):
    async def send_command_help(self, command: Command):
        embed = Embed()
        embed.title = command.name.capitalize()
        embed.description = command.brief

        embed.add_field(name='Description', value=command.description)

        dest = super().get_destination()
        await dest.send(embed=embed)

    async def send_bot_help(self, mapping):
        commands = mapping.get(None)

        embed = Embed()
        embed.title = 'Help'
        embed.description = 'Commands can only be used in NSFW channels'

        prefix = super().clean_prefix

        for cmd in commands:
            if cmd != self:
                embed.add_field(name=f'{prefix}{cmd.name}', value=cmd.brief, inline=False)

        dest = super().get_destination()
        return await dest.send(embed=embed)
