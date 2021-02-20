from typing import Optional, List

from discord import User
from discord.ext import commands
from discord.ext.commands import Cog, Context

from api.post_data import PostData
from db.repo import get_favorites, remove_favorite


class PostsEmbedMessage:
    message = None
    page = 0

    def __init__(self, ctx: Context, data: List[PostData]):
        self.ctx = ctx
        self.data = data

    async def create_message(self):
        data = self.data[self.page]
        self.message = await self.ctx.send(**data.to_content())

        await self.message.add_reaction('⬅')
        await self.message.add_reaction('➡')
        await self.message.add_reaction('🗑️')

        self.ctx.bot.add_listener(self.on_reaction_add)

    async def on_reaction_add(self, reaction, user):
        if user == self.ctx.bot.user or self.message.id != reaction.message.id:
            return

        if reaction.emoji == '➡':
            self.page = (self.page + 1) % len(self.data)
            await self.update_message()
        if reaction.emoji == '⬅':
            self.page = (self.page - 1) % len(self.data)
            await self.update_message()
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
        data = self.get_data()
        await self.message.edit(**data.to_content())

    def get_data(self):
        return self.data[self.page]


class Favorites(Cog):
    @commands.command(name='favorites', aliases=['favs'], brief='List a users favorites')
    async def favorites(self, ctx: Context, user: Optional[User] = None):
        user = user or ctx.author
        favorites = get_favorites(user)

        if favorites:
            post_embed_message = PostsEmbedMessage(ctx, favorites)
            await post_embed_message.create_message()
        else:
            await ctx.send('No favorites found')
