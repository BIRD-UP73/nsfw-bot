from discord import Member
from discord.ext.commands import Context, is_nsfw

from commands.nsfw.site.nsfw_command import NsfwCommand, default_emojis
from db import post_repository
from posts.post_message.favorites_message import FavoritesMessage


class Favorites(NsfwCommand):
    name = 'favorites'
    aliases = ['favs']
    brief = 'Shows a user\'s favorites'
    emojis = default_emojis + ['⛔']
    check_tags = False

    @is_nsfw()
    async def func(self, ctx: Context, user: Member = None):
        user = user or ctx.author
        fav_list = post_repository.get_favorites(user)

        if not fav_list:
            return await ctx.send('No favorites found')

        await FavoritesMessage(ctx, fav_list, self.emojis).create_message()
