from typing import List

from discord import User
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from api.page_embed_message import PageEmbedMessage
from api.post_entry import PostEntry
from db.post_repository import get_favorites, remove_favorite


class FavoritesMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, user: User, data: List[PostEntry]):
        super().__init__(ctx, data)
        self.user = user

    async def on_reaction_add(self, reaction, user):
        if user == self.ctx.bot.user or self.message.id != reaction.message.id:
            return

        await super().on_reaction_add(reaction, user)

        data = self.get_data()

        if reaction.emoji == '🗑️' and user == self.user:
            remove_favorite(self.ctx.author, data.url, data.post_id)
            await self.ctx.send(f'{self.ctx.author.mention}, removed favorite successfully.')
            self.data.remove(self.data[self.page])

            if len(self.data) == 0:
                await self.message.edit(content='No favorites found', embed=None)
                await self.message.clear_reactions()
                self.ctx.bot.remove_listener(self.on_reaction_add)
            else:
                self.page = 0
                await self.update_message()

        await super().after_reaction(reaction, user)

    def get_current_page(self) -> dict:
        data = self.get_data()
        post = data.fetch_post()

        if post.is_animated():
            return post.to_content()

        embed = post.to_embed()
        embed.title = 'Favorites'
        embed.description = f'Favorites for {self.ctx.author.mention}'
        embed.timestamp = data.saved_at

        embed.set_footer(text=f'Page {self.page + 1} of {len(self.data)}')

        return dict(content=None, embed=embed)


def parse_favorites(fav_list: List[tuple]) -> List[PostEntry]:
    return [PostEntry(tup[0], tup[1], tup[2]) for tup in fav_list]


class Favorites(Cog):

    description = """
    List a users favorites.
    
    Emojis 
    ⭐   add post to your favorites
    🗑️  remove this post from your favorites list
    ⬅➡ scroll through pages
    """

    @is_nsfw()
    @commands.command(name='favorites', aliases=['favs'], description=description)
    async def favorites(self, ctx: Context, user: User = None):
        user = user or ctx.author
        favorites = parse_favorites(get_favorites(user))

        if favorites:
            post_embed_message = FavoritesMessage(ctx, user, favorites)
            return await post_embed_message.create_message()

        await ctx.send('No favorites found')
