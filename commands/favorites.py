from discord import Member
from discord.ext.commands import Context, is_nsfw, command

from db import post_repository
from posts.post_message.favorites_message import FavoritesMessage


@is_nsfw()
@command(name='favorites', aliases=['favs'], brief='Shows a user\'s favorites')
async def favorites(ctx: Context, user: Member = None):
    user = user or ctx.author
    fav_list = post_repository.get_favorites(user)

    if not favorites:
        return await ctx.send('No favorites found')

    await FavoritesMessage(ctx, fav_list).create_message()
