from abc import ABC
from typing import Union

from discord import Reaction, Member, User

from posts.message.reaction_handler import EmptyReactionHandler, ReactionContext


class AbstractPost(ABC):
    reaction_handlers = {}

    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        reaction_context = ReactionContext(reaction, user, self)

        handler = self.reaction_handlers.get(reaction.emoji, EmptyReactionHandler())
        await handler.on_reaction(reaction_context)
