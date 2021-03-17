from abc import abstractmethod, ABC
from typing import Union

from discord import User, Message, DMChannel, TextChannel, Member, Reaction
from discord.ext.commands import Context, Bot

from posts.data.post_data import PostData, PostHasDisallowedTags
from posts.message.reaction_handler import ReactionHandler, ReactionContext, \
    DeleteMessageReactionHandler, AddFavoriteReactionHandler, EmptyReactionHandler


class RandomPostReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        await ctx.post.update_message()


class PostMessage(ABC):
    message: Message = None
    post_data: PostData = None

    reaction_handlers = {
        '🔁': RandomPostReactionHandler(author_only=True),
        '🗑️': DeleteMessageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, url: str, tags: str):
        self.bot: Bot = ctx.bot
        self.channel: Union[TextChannel, DMChannel] = ctx.channel
        self.author: Union[User, Member] = ctx.author
        self.url: str = url
        self.tags: str = tags

    async def create_message(self):
        """
        Creates a message with the post, and adds reaction listeners
        """
        self.post_data = self.get_post()

        message_content = self.post_data.to_message_content()
        self.message = await self.channel.send(**message_content.to_dict())

        self.bot.add_listener(self.on_reaction_add)

        for emoji in self.reaction_handlers:
            await self.message.add_reaction(emoji)

    async def update_message(self):
        self.post_data = self.get_post()
        await self.message.edit(**self.post_data.to_message_content().to_dict())

    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        reaction_context = ReactionContext(reaction, user, self)

        handler = self.reaction_handlers.get(reaction.emoji, EmptyReactionHandler())
        await handler.on_reaction(reaction_context)

    def update_hist(self, post_data: PostData):
        """
        Adds the current post to the post history
        """
        hist_cog = self.bot.get_cog('PostHist')
        hist_cog.add_to_history(self.channel, self.url, post_data)

    def get_data(self):
        return self

    def get_post(self) -> PostData:
        post_data = self.fetch_post()
        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data

    @abstractmethod
    def fetch_post(self) -> PostData:
        """
        Abstract method to fetch a post, should return :class:`PostData`
        """
        pass
