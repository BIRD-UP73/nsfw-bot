from discord.ext.commands import Context

from commands.custom_command import CustomCommand


class Github(CustomCommand):
    name = 'github'
    brief = 'Shows GitHub repository url'
    aliases = ['git']

    async def func(self, ctx: Context):
        await ctx.send('https://github.com/BIRD-UP73/nsfw-bot')
