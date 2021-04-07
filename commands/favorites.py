from discord import Member
from discord.ext import commands
from discord.ext.commands import Context, is_nsfw

from db import post_repository
from posts.message.favorites_message import FavoritesMessage

description = """
List a users favorites.

Emojis 
⭐   add post to your favorites
🗑️  remove this post from your favorites list
⬅➡ scroll through pages
"""


@is_nsfw()
@commands.command(name='favorites', aliases=['favs'], description=description)
async def favorites(ctx: Context, user: Member = None):
    user = user or ctx.author
    fav_list = post_repository.get_favorites(user)

    if not favorites:
        return await ctx.send('No favorites found')

    await FavoritesMessage(ctx, fav_list, user).create_message()
