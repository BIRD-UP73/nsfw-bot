from typing import Optional, List

from discord import User, Embed
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from api.post_entry import PostEntry
from db.post_repository import get_favorites, remove_favorite
from util.embed_util import PageEmbedMessage


class FavoritesMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, data):
        super().__init__(ctx, data)

    async def on_reaction_add(self, reaction, user):
        if user == self.ctx.bot.user or self.message.id != reaction.message.id:
            return

        await super().on_reaction_add(reaction, user)

        if reaction.emoji == '🗑️' and user == self.ctx.author:
            data = self.get_data()

            if remove_favorite(self.ctx.author, data.url, data.post_id):
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

    def get_current_page(self) -> dict:
        content = self.get_data().to_content()

        if content.get('embed'):
            embed: Embed = content.get('embed')
            embed.title = 'Favorites'
            embed.description = f'Favorites for {self.ctx.author.mention}'
            embed.set_footer(text=f'Page {self.page + 1} of {len(self.data)}')

        return content


def parse_favorites(fav_list: List[tuple]):
    return [PostEntry(tup[0], tup[1]) for tup in fav_list]


class Favorites(Cog):

    @is_nsfw()
    @commands.command(name='favorites', aliases=['favs'], brief='List a users favorites')
    async def favorites(self, ctx: Context, user: Optional[User] = None):
        user = user or ctx.author
        favorites = parse_favorites(get_favorites(user))

        if favorites:
            post_embed_message = FavoritesMessage(ctx, favorites)
            await post_embed_message.create_message()
        else:
            await ctx.send('No favorites found')
