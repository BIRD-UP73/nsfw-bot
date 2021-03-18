from typing import List, Union

from discord import User, Reaction, Member
from discord.ext import commands
from discord.ext.commands import Cog, Context, is_nsfw

from db import post_repository
from posts.data.post_entry import PostEntry
from posts.message.page_embed_message import PageEmbedMessage
from posts.message.post_message_content import PostMessageContent


class FavoritesMessage(PageEmbedMessage):
    def __init__(self, ctx: Context, user: User, data: List[PostEntry]):
        super().__init__(ctx, data)
        self.user = user

    async def add_favorite(self, user):
        if user == self.author:
            return True

        await super().add_favorite(user)
        return True

    async def handle_reaction(self, reaction: Reaction, user: Union[Member, User]) -> bool:
        result = await super().handle_reaction(reaction, user)

        if result:
            return result

        if reaction.emoji == '🗑️':
            await self.remove_favorite(user)
            return True

    async def remove_favorite(self, user: User):
        if user != self.user:
            return

        data = self.get_data()

        post_repository.remove_favorite(user, data.url, data.post_id)
        await self.channel.send(f'{user.mention}, removed favorite successfully.')
        self.data.remove(data)

        if len(self.data) == 0:
            return await self.clear_message()

        if self.page == len(self.data):
            self.page = 0

        await self.update_message()
        return False

    def page_content(self) -> PostMessageContent:
        data = self.get_data()
        post_data = data.fetch_post()

        message_content = post_data.to_message_content()

        if message_content.embed:
            message_content.embed.title = 'Favorites'
            message_content.embed.description = f'Favorites for {self.user.mention}'
            message_content.embed.timestamp = data.saved_at
            message_content.embed.set_footer(text=f'Page {self.page + 1} of {len(self.data)}')

        return message_content

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

        post_embed_message = FavoritesMessage(ctx, user, favorites)
        await post_embed_message.create_message()
