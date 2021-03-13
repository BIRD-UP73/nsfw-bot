from abc import ABC
from typing import Union

from discord import User, Message, DMChannel, TextChannel, Member, Reaction
from discord.ext.commands import Context, Bot

from posts.data.post_data import PostData, PostHasDisallowedTags
from posts.message.reaction_handler import ReactionHandler, ReactionContext, \
    DeleteMessageReactionHandler, AddFavoriteReactionHandler, EmptyReactionHandler
from posts.post.post_fetcher import PostMessageFetcher


class RandomPostReactionHandler(ReactionHandler):
    async def handle_reaction(self, ctx: ReactionContext):
        ctx.post.post_data = ctx.post.get_post()
        await ctx.post.message.edit(**ctx.post.post_content())


class PostMessage(ABC):
    message: Message = None
    post_data: PostMessageFetcher = None

    reaction_handlers = {
        '🔁': RandomPostReactionHandler(author_only=True),
        '🗑️': DeleteMessageReactionHandler(),
        '⭐': AddFavoriteReactionHandler()
    }

    def __init__(self, ctx: Context, fetcher: PostMessageFetcher):
        self.bot: Bot = ctx.bot
        self.channel: Union[TextChannel, DMChannel] = ctx.channel
        self.author: Union[User, Member] = ctx.author
        self.fetcher: PostMessageFetcher = fetcher

    async def create_message(self):
        """
        Creates a message with the post, and adds reaction listeners
        """
        self.message = await self.channel.send(**self.post_content())

        self.bot.add_listener(self.on_reaction_add)

        for emoji in self.reaction_handlers:
            await self.message.add_reaction(emoji)

    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        reaction_context = ReactionContext(reaction, user, self)

        handler = self.reaction_handlers.get(reaction.emoji, EmptyReactionHandler())
        await handler.on_reaction(reaction_context)

    def update_hist(self, post_data):
        """
        Adds the current post to the post history
        """
        hist_cog = self.bot.get_cog('PostHist')
        hist_cog.add_to_history(self.channel, self.fetcher.url, post_data.post_id)

    def post_content(self) -> dict:
        post_data = self.get_post()

        if post_data.is_animated():
            return dict(content=post_data.to_text(), embed=None)

        return dict(content=None, embed=post_data.to_embed())

    def get_data(self):
        return self

    def get_post(self) -> PostData:
        post_data = self.fetcher.fetch_post()
        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data
