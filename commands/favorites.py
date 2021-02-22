from typing import Optional, List

from discord import User
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from api.post_data import PostData
from db.repo import get_favorites, remove_favorite
from page_embed_message import PageEmbedMessage


class FavoritesMessage(PageEmbedMessage):

    def __init__(self, ctx: Context, data: List[PostData]):
        super().__init__(ctx, data)

    async def on_reaction_add(self, reaction, user):
        await super().on_reaction_add(reaction, user)

        if reaction.emoji == '🗑️' and user == self.ctx.author:
            if remove_favorite(self.ctx.author, self.get_data()):
                await self.ctx.send(f'{self.ctx.author.mention}, removed favorite successfully.')

            self.data.remove(self.data[self.page])

            if len(self.data) == 0:
                await self.message.edit(content='No favorites found', embed=None)
                await self.message.clear_reactions()
                self.ctx.bot.remove_listener(self.on_reaction_add)
            else:
                self.page = 0
                await self.update_message()

        if self.ctx.guild:
            await self.message.remove_reaction(reaction, user)

    async def update_message(self):
        content = self.get_data().to_content()

        if embed := content.get('embed'):
            embed.description = f'Favorites for {self.ctx.author.mention}. Page {self.page + 1} of {len(self.data)}'

        await self.message.edit(**content)

    def get_data(self) -> PostData:
        return self.data[self.page]


class Favorites(Cog):

    @is_nsfw()
    @commands.command(name='favorites', aliases=['favs'], brief='List a users favorites')
    async def favorites(self, ctx: Context, user: Optional[User] = None):
        user = user or ctx.author
        favorites = get_favorites(user)

        if favorites:
            post_embed_message = FavoritesMessage(ctx, favorites)
            await post_embed_message.create_message()
        else:
            await ctx.send('No favorites found')
