from typing import List

from discord import User
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from posts.message.page_embed_message import PageEmbedMessage
from posts.data.post_entry import PostEntry
from posts.message.reaction_handler import ReactionHandler, ReactionContext
from db import post_repository


class RemoveFavoriteReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.user != ctx.post.user:
            return

        data = ctx.post.get_data()

        post_repository.remove_favorite(ctx.user, data.url, data.post_id)
        await ctx.post.channel.send(f'{ctx.user.mention}, removed favorite successfully.')
        ctx.post.data.remove(data)

        if len(ctx.post.data) == 0:
            await ctx.post.message.edit(content='No favorites found', embed=None)
            await ctx.post.message.clear_reactions()
            ctx.post.bot.remove_listener(ctx.post.on_reaction_add)
            return

        if ctx.post.page == len(ctx.post.data):
            ctx.post.page = 0

        await ctx.post.update_message()


class FavoritesMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, user: User, data: List[PostEntry]):
        super().__init__(ctx, data)
        self.user = user
        self.author = ctx.author
        self.reaction_handlers['🗑️'] = RemoveFavoriteReactionHandler()

    def get_current_page(self) -> dict:
        data = self.get_data()
        self.post_data = data.fetch_post()

        if self.post_data.is_animated():
            return self.post_data.to_content()

        embed = self.post_data.to_embed()
        embed.title = 'Favorites'
        embed.description = f'Favorites for {self.author.mention}'
        embed.timestamp = data.saved_at

        embed.set_footer(text=f'Page {self.page + 1} of {len(self.data)}')

        return dict(content=None, embed=embed)


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
        favorites = post_repository.get_favorites(user)

        if favorites:
            post_embed_message = FavoritesMessage(ctx, user, favorites)
            return await post_embed_message.create_message()

        await ctx.send('No favorites found')
