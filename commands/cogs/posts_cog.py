from typing import Optional

from discord import TextChannel
from discord.ext.commands import Cog, Context, NSFWChannelRequired, UserInputError

from commands.nsfw_command import nsfw_command
from posts.post_message.factory.post_message_factory import PostMessageFactory
from util import tag_util


class PostCog(Cog):
    @nsfw_command(name='rule34', aliases=['r34'])
    async def rule34(self, ctx: Context, score: Optional[int] = 50, *, tags: str = ''):
        await PostMessageFactory.create_xml_post(ctx, tags, score, 200000)

    @nsfw_command(name='xbooru')
    async def xbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str = ''):
        await PostMessageFactory.create_xml_post(ctx, tags, score)

    @nsfw_command(name='gelbooru')
    async def gelbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str = ''):
        await PostMessageFactory.create_xml_post(ctx, tags, score, 20000)

    @nsfw_command(name='tbib')
    async def tbib(self, ctx: Context, score: Optional[int] = 0, *, tags: str = ''):
        await PostMessageFactory.create_xml_post(ctx, tags, score)

    @nsfw_command(name='danbooru', aliases=['dbooru'])
    async def danbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str = ''):
        await PostMessageFactory.create_json_post(ctx, tags, score)

    async def cog_before_invoke(self, ctx):
        tags = ctx.kwargs.get('tags')
        disallowed_tags = tag_util.get_disallowed_tags(tags)

        if len(disallowed_tags) > 0:
            tag_txt = ', '.join(disallowed_tags)
            raise UserInputError(f'You are not allowed to search for: {tag_txt}')

    def cog_check(self, ctx):
        ch = ctx.channel
        if not ctx.guild or (isinstance(ch, TextChannel) and ch.is_nsfw()):
            return True

        raise NSFWChannelRequired(ch)
