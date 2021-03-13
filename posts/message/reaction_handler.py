from abc import ABC, abstractmethod
from typing import Union

from discord import Reaction, Member, User, ClientUser

from db import post_repository


class ReactionContext:
    def __init__(self, reaction: Reaction, user: Union[Member, User], post):
        self.reaction: Reaction = reaction
        self.user: Union[Member, User] = user
        self.post = post

    @property
    def bot_user(self) -> ClientUser:
        return self.post.bot.user


class ReactionHandler(ABC):
    def __init__(self, **kwargs):
        self.delete_reaction = kwargs.get('delete_reaction', True)
        self.author_only = kwargs.get('author_only', False)

    async def on_reaction(self, ctx: ReactionContext):
        if ctx.user == ctx.bot_user or ctx.post.message.id != ctx.reaction.message.id:
            return
        if not self.author_only or ctx.user == ctx.post.author:
            await self.handle_reaction(ctx)

        if self.delete_reaction and ctx.post.message.guild:
            await self.remove_reaction(ctx)

    @staticmethod
    async def remove_reaction(ctx: ReactionContext):
        await ctx.post.message.remove_reaction(ctx.reaction.emoji, ctx.user)

    @abstractmethod
    async def handle_reaction(self, ctx: ReactionContext):
        """
        Function used for reaction-specific handling

        :param ctx: the reaction context
        """
        pass


class EmptyReactionHandler(ReactionHandler):
    """
    Reaction handler without any specific handling
    Used by default
    """
    async def handle_reaction(self, ctx: ReactionContext):
        return


class DeleteMessageReactionHandler(ReactionHandler):
    def __init__(self, author_only=False):
        super().__init__(author_only=author_only, delete_reaction=False)

    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.user != ctx.post.author:
            return await self.remove_reaction(ctx)

        await ctx.post.message.delete()
        ctx.post.bot.remove_listener(ctx.post.on_reaction_add)


class AddFavoriteReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        fetcher = ctx.post.fetcher
        post_data = ctx.post.fetcher.post_data

        if post_data.is_error() or post_repository.exists(ctx.user, fetcher.url, post_data.post_id):
            return

        post_repository.store_favorite(ctx.user, fetcher.url, post_data.post_id)
        await ctx.post.channel.send(f'{ctx.user.mention}, successfully stored favorite.')
