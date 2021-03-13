from discord import User
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from db import post_repository
from posts.message.page_embed_message import PageEmbedMessage
from posts.message.reaction_handler import ReactionHandler, ReactionContext
from posts.post.post_fetcher import PostEntryFetcher


class RemoveFavoriteReactionHandler(ReactionHandler):
    post: PageEmbedMessage

    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.user != ctx.post.user:
            return

        fetcher = ctx.post.fetcher
        data = fetcher.post_data

        post_repository.remove_favorite(ctx.user, fetcher.url, data.post_id)
        await ctx.post.channel.send(f'{ctx.user.mention}, removed favorite successfully.')

        ctx.post.fetcher.remove_current_post()

        if len(ctx.post.fetcher.entries) == 0:
            return await ctx.post.clear_message()

        if len(ctx.post.fetcher.entries) == ctx.post.fetcher.page:
            ctx.post.fetcher.page = 0

        await ctx.post.update_message()


class FavoritesMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, user: User, fetcher: PostEntryFetcher):
        super().__init__(ctx, fetcher)
        self.user = user
        self.author = ctx.author
        self.reaction_handlers['🗑️'] = RemoveFavoriteReactionHandler()

    def get_current_page(self) -> dict:
        entry = self.fetcher.current_entry()
        post_data = self.fetcher.fetch_post()

        if post_data.is_animated():
            return dict(content=post_data.to_text(), embed=None)

        embed = post_data.to_embed()
        embed.title = 'Favorites'
        embed.description = f'Favorites for {self.user.mention}'
        embed.timestamp = entry.saved_at

        embed.set_footer(text=f'Page {self.fetcher.page + 1} of {len(self.fetcher.entries)}')

        return dict(content=None, embed=embed)

    async def clear_message(self):
        self.bot.remove_listener(self.on_reaction_add)
        await self.message.clear_reactions()
        await self.message.edit(content='No favorites.', embed=None)


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

        if not favorites:
            return await ctx.send('No favorites found')

        post_fetcher = PostEntryFetcher(favorites)
        post_embed_message = FavoritesMessage(ctx, user, post_fetcher)
        await post_embed_message.create_message()
