from typing import List

from discord import User
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from api.page_embed_message import PageEmbedMessage
from api.post_entry import PostEntry
from api.reaction_handler import ReactionHandler, ReactionContext
from db.post_repository import get_favorites, remove_favorite


class RemoveFavoriteReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.user != ctx.post.user:
            return

        data = ctx.post.get_data()

        remove_favorite(ctx.user, data.url, data.post_id)
        await ctx.post.ctx.send(f'{ctx.user.mention}, removed favorite successfully.')
        ctx.post.data.remove(data)

        if len(ctx.post.data) == 0:
            await ctx.post.message.edit(content='No favorites found', embed=None)
            await ctx.post.message.clear_reactions()
            ctx.post.ctx.bot.remove_listener(ctx.post.on_reaction_add)
            return

        ctx.post.page = 0
        await ctx.post.update_message()


class FavoritesMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, user: User, data: List[PostEntry]):
        super().__init__(ctx, data)
        self.user = user
        self.reaction_handlers['🗑️'] = RemoveFavoriteReactionHandler()

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
