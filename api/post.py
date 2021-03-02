from abc import ABC, abstractmethod

from discord import Reaction, User, Message
from discord.ext.commands import Context

from api.post_data import PostData
from api.reaction_handler import ReactionHandler, ReactionContext, EmptyReactionHandler, DeleteMessageReactionHandler
from db import post_repository


class RandomPostReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.user != ctx.post.ctx.author:
            return

        ctx.post.post_data = ctx.post.fetch_post()
        await ctx.post.message.edit(**ctx.post.post_data.to_content())


class AddFavoriteReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        if ctx.post.post_data.is_error() or\
                post_repository.exists(ctx.user, ctx.post.url, ctx.post.post_data.id):
            return

        post_repository.store_favorite(ctx.user, ctx.post.url, ctx.post.post_data.id)
        await ctx.post.ctx.send(f'{ctx.user.mention}, added post to favorites')


class AbstractPost(ABC):
    ctx: Context = None
    message: Message = None
    post_data: PostData = None
    url: str = None
    tags: str = None

    reaction_handlers = {
        '🔁': RandomPostReactionHandler(author_only=True),
        '🗑️': DeleteMessageReactionHandler(author_only=True),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, url: str, tags: str):
        self.ctx = ctx
        self.url = url
        self.tags = tags

    async def create_message(self):
        """
        Creates a message with the post, and adds reaction listeners
        """
        self.post_data = self.fetch_post()
        self.message = await self.ctx.send(**self.post_data.to_content())

        self.ctx.bot.add_listener(self.on_reaction_add)

        for emoji in self.reaction_handlers:
            await self.message.add_reaction(emoji)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        reaction_context = ReactionContext(reaction, user, self)

        handler = self.reaction_handlers.get(reaction.emoji, EmptyReactionHandler())
        await handler.on_reaction(reaction_context)

    def update_hist(self, post_data):
        """
        Adds the current post to the post history
        """
        hist_cog = self.ctx.bot.get_cog('PostHist')

        target = self.ctx.guild or self.ctx.channel
        hist_cog.add_post(target, self.url, post_data.id)

    @abstractmethod
    def fetch_post(self) -> PostData:
        """
        Abstract method to fetch a post, should return :class:`PostData`
        """
        pass
