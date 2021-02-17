from discord import RawReactionActionEvent
from discord.ext.commands import Bot, Cog, Context


class Listeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is ready')

    @Cog.listener()
    async def on_command_error(self, ctx: Context, exception: Exception):
        await ctx.send(str(exception))
        raise exception

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        if payload.emoji.name == '🗑️':
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            if message.author == self.bot.user:
                await message.delete()
