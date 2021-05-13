from datetime import datetime

from discord import Embed
from discord.ext.commands import Context

from commands.custom_command import CustomCommand


class Latency(CustomCommand):
    name = 'latency'
    aliases = ['hello', 'ping']
    brief = 'Shows message latency'

    async def func(self, ctx: Context):
        embed = Embed(title='Latency')

        latency_ms = int(ctx.bot.latency * 1000)
        embed.add_field(name='Websocket', value=f'{latency_ms} ms')

        before = datetime.now()
        msg = await ctx.send(embed=embed)
        diff = datetime.now() - before

        embed.add_field(name='Send', value=f'{diff.microseconds // 1000} ms')

        msg_diff = msg.created_at - ctx.message.created_at
        embed.add_field(name='Message', value=f'{msg_diff.microseconds // 1000} ms')

        await msg.edit(embed=embed)
