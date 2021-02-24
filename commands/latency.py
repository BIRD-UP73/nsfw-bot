from datetime import datetime

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context


@commands.command(name='latency', aliases=['ping'])
async def latency(ctx: Context):
    embed = Embed()
    embed.title = 'Latency'

    latency_ms = int(ctx.bot.latency * 1000)
    embed.add_field(name='Websocket', value=f'{latency_ms} ms')

    before = datetime.now()
    msg = await ctx.send(embed=embed)
    diff = datetime.now() - before

    embed.add_field(name='Send', value=f'{diff.microseconds // 1000} ms')

    msg_diff = msg.created_at - ctx.message.created_at
    embed.add_field(name='Message', value=f'{msg_diff.microseconds // 1000} ms')

    await msg.edit(embed=embed)
