from typing import List

from discord import Game, Message
from discord.ext.commands import Bot, Cog, Context

from posts.post.abstract_post import AbstractPost


class Listeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.posts: List[AbstractPost] = []

    @Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is ready')

        help_game = Game(name=f'{self.bot.command_prefix}help')
        await self.bot.change_presence(activity=help_game)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, exception: Exception):
        await ctx.send(str(exception))
        raise exception

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        for post in self.posts:
            if post.message.id == message.id:
                self.posts.remove(post)

    def add_post(self, post: AbstractPost):
        self.posts.append(post)
