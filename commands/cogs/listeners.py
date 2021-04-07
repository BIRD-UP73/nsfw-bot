from discord import Game
from discord.ext.commands import Bot, Cog, Context


class Listeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is ready')

        help_game = Game(name=f'{self.bot.command_prefix}help')
        await self.bot.change_presence(activity=help_game)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, exception: Exception):
        await ctx.send(str(exception))
        raise exception
