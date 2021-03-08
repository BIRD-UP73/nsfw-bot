from abc import abstractmethod
from typing import List, Dict, Union, Deque

from discord import TextChannel, Member, User, Message, DMChannel, Reaction
from discord.ext.commands import Context, Bot

from posts.data.post_data import PostData
from posts.data.post_entry import PostEntry
from posts.message.reaction_handler import ReactionContext, ReactionHandler, EmptyReactionHandler, \
    AddFavoriteReactionHandler
from posts.post.abstract_post import AbstractPost


class NextPageReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        ctx.post.page = (ctx.post.page + 1) % len(ctx.post.data)
        await ctx.post.update_message()


class PreviousPageReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        ctx.post.page = (ctx.post.page - 1) % len(ctx.post.data)
        await ctx.post.update_message()


class PageEmbedMessage(AbstractPost):
    message: Message = None
    page: int = 0
    post_data: PostData = None

    reaction_handlers: Dict[str, ReactionHandler] = {
        '⬅': PreviousPageReactionHandler(),
        '➡': NextPageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, data: Union[List[PostEntry], Deque[PostEntry]]):
        self.bot: Bot = ctx.bot
        self.author: Union[User, Member] = ctx.author
        self.channel: Union[DMChannel, TextChannel] = ctx.channel
        self.data: Union[List[PostEntry], Deque[PostEntry]] = data

    async def create_message(self):
        page_content = self.get_current_page()
        self.message = await self.channel.send(**page_content)

        self.bot.add_listener(self.on_reaction_add)

        for reaction_emoji in self.reaction_handlers:
            await self.message.add_reaction(reaction_emoji)

    async def update_message(self):
        page_content = self.get_current_page()
        await self.message.edit(**page_content)

    def get_data(self) -> PostEntry:
        return self.data[self.page]

    @abstractmethod
    def get_current_page(self) -> dict:
        """
        Returns the content of the current page of the embed
        This should be in the form of a :type mapping: dict
        with both a 'content' and an 'embed' field

        :return: the content of the page
        """
        pass
