from abc import ABC, abstractmethod
from typing import Union

from discord import Reaction, Member, User


class ReactionContext:
    def __init__(self, reaction: Reaction, user: Union[Member, User], post):
        self.reaction = reaction
        self.user = user
        self.post = post

    @property
    def bot_user(self):
        return self.post.ctx.bot.user


class ReactionHandler(ABC):
    def __init__(self, delete_reaction=True, author_only=False):
        self.delete_reaction = delete_reaction
        self.author_only = author_only

    async def on_reaction(self, ctx: ReactionContext):
        if ctx.user == ctx.bot_user or ctx.post.message.id != ctx.reaction.message.id:
            return
        if self.author_only and ctx.user != ctx.post.ctx.author:
            await self.remove_reaction(ctx)
            return

        await self.handle_reaction(ctx)

        if self.delete_reaction and ctx.post.message.guild:
            await self.remove_reaction(ctx)

    async def remove_reaction(self, ctx: ReactionContext):
        await ctx.post.message.remove_reaction(ctx.reaction.emoji, ctx.user)

    @abstractmethod
    async def handle_reaction(self, ctx: ReactionContext):
        pass


class EmptyReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        return


class DeleteMessageReactionHandler(ReactionHandler):
    def __init__(self, author_only=False):
        super().__init__(author_only=author_only, delete_reaction=False)

    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.user != ctx.post.ctx.author:
            await self.remove_reaction(ctx)
            return

        await ctx.post.message.delete()
        ctx.post.ctx.bot.remove_listener(ctx.post.on_reaction_add)
