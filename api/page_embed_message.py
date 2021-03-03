from abc import ABC, abstractmethod
from typing import List, Dict

from discord import Reaction
from discord.ext.commands import Context

from api.post_entry import PostEntry
from api.reaction_handler import ReactionContext, ReactionHandler, EmptyReactionHandler, AddFavoriteReactionHandler


class NextPageReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        ctx.post.page = (ctx.post.page + 1) % len(ctx.post.data)
        await ctx.post.update_message()


class PreviousPageReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        ctx.post.page = (ctx.post.page - 1) % len(ctx.post.data)
        await ctx.post.update_message()


class PageEmbedMessage(ABC):
    message = None
    page = 0
    post_data = None

    reaction_handlers: Dict[str, ReactionHandler] = {
        '⬅': PreviousPageReactionHandler(),
        '➡': NextPageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, data: List[PostEntry]):
        self.ctx: Context = ctx
        self.data: List[PostEntry] = data

    async def create_message(self):
        self.message = await self.ctx.send(**self.get_current_page())

        for reaction_emoji in self.reaction_handlers:
            await self.message.add_reaction(reaction_emoji)

        self.ctx.bot.add_listener(self.on_reaction_add)

    async def on_reaction_add(self, reaction, user):
        reaction_context = ReactionContext(reaction, user, self)

        handler = self.reaction_handlers.get(reaction.emoji, EmptyReactionHandler())
        await handler.on_reaction(reaction_context)

    async def update_message(self):
        page_content = self.get_current_page()
        await self.message.edit(**page_content)

    def get_data(self) -> PostEntry:
        return self.data[self.page]

    @abstractmethod
    def get_current_page(self) -> dict:
        pass
