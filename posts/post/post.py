from abc import ABC, abstractmethod

from discord import Reaction, User, Message
from discord.ext.commands import Context

from posts.data.post_data import PostData
from posts.message.reaction_handler import ReactionHandler, ReactionContext, EmptyReactionHandler, \
    DeleteMessageReactionHandler, AddFavoriteReactionHandler


class RandomPostReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        ctx.post.post_data = ctx.post.fetch_post()
        await ctx.post.message.edit(**ctx.post.post_data.to_content())


class AbstractPost(ABC):
    message: Message = None
    post_data: PostData = None
    url: str = None
    tags: str = None

    reaction_handlers = {
        '🔁': RandomPostReactionHandler(author_only=True),
        '🗑️': DeleteMessageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, url: str, tags: str):
        self.bot = ctx.bot
        self.channel = ctx.channel
        self.author = ctx.author
        self.guild = ctx.guild
        self.url = url
        self.tags = tags

    async def create_message(self):
        """
        Creates a message with the post, and adds reaction listeners
        """
        self.post_data = self.fetch_post()
        self.message = await self.channel.send(**self.post_data.to_content())

        self.bot.add_listener(self.on_reaction_add)

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
        target = self.guild or self.channel

        hist_cog = self.bot.get_cog('PostHist')
        hist_cog.add_post(target, self.url, post_data.post_id)

    def get_data(self):
        return self

    @abstractmethod
    def fetch_post(self) -> PostData:
        """
        Abstract method to fetch a post, should return :class:`PostData`
        """
        pass
