from abc import ABC
from typing import Dict, Union

from discord import Member, User, Message
from discord.ext.commands import Context

from posts.data.post_data import PostData
from posts.message.reaction_handler import ReactionContext, ReactionHandler, AddFavoriteReactionHandler
from posts.post.post_fetcher import PostEntryFetcher
from posts.post.post_message import Post


class NextPageReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        page = (ctx.post.fetcher.page + 1) % len(ctx.post.fetcher.entries)
        ctx.post.fetcher.set_page(page)
        await ctx.post.update_message()


class PreviousPageReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        page = (ctx.post.fetcher.page - 1) % len(ctx.post.fetcher.entries)
        ctx.post.fetcher.set_page(page)
        await ctx.post.update_message()


class PageEmbedMessage(Post, ABC):
    message: Message = None

    reaction_handlers: Dict[str, ReactionHandler] = {
        '⬅': PreviousPageReactionHandler(),
        '➡': NextPageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, fetcher: PostEntryFetcher):
        super().__init__(ctx)
        self.author: Union[User, Member] = ctx.author
        self.fetcher = fetcher

    def get_post(self) -> PostData:
        return self.fetcher.fetch_post()
