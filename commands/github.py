from discord.ext.commands import command, Context


@command(name='github', brief='Show GitHub repository url')
async def github(ctx: Context):
    await ctx.send('https://github.com/BIRD-UP73/nsfw-bot')
