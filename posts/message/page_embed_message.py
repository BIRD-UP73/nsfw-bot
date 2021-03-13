from abc import ABC
from typing import Dict, Union

from discord import TextChannel, Member, User, Message, DMChannel, Reaction
from discord.ext.commands import Context, Bot

from posts.message.reaction_handler import ReactionContext, ReactionHandler, EmptyReactionHandler, \
    AddFavoriteReactionHandler
from posts.post.post_fetcher import PostEntryFetcher


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


class PageEmbedMessage(ABC):
    message: Message = None

    reaction_handlers: Dict[str, ReactionHandler] = {
        '⬅': PreviousPageReactionHandler(),
        '➡': NextPageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, fetcher: PostEntryFetcher):
        self.bot: Bot = ctx.bot
        self.author: Union[User, Member] = ctx.author
        self.channel: Union[DMChannel, TextChannel] = ctx.channel
        self.fetcher = fetcher

    async def create_message(self):
        page_content = self.get_current_page()
        self.message = await self.channel.send(**page_content)

        self.bot.add_listener(self.on_reaction_add)

        for reaction_emoji in self.reaction_handlers:
            await self.message.add_reaction(reaction_emoji)

    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        reaction_context = ReactionContext(reaction, user, self)

        handler = self.reaction_handlers.get(reaction.emoji, EmptyReactionHandler())
        await handler.on_reaction(reaction_context)

    async def update_message(self):
        page_content = self.get_current_page()
        await self.message.edit(**page_content)

    def get_current_page(self) -> dict:
        """
        Returns the content of the current page of the embed
        This should be in the form of a :type mapping: dict
        with both a 'content' and an 'embed' field

        :return: the content of the page
        """
        return self.fetcher.fetch_post()
