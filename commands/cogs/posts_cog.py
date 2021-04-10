from typing import Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, NSFWChannelRequired, UserInputError

from posts.post.factory.post_factory import PostFactory
from util import tag_util
from util.url_util import short_urls

desc = {
    'danbooru': """
    Searches images from danbooru.com
    
    Emojis 
    ⭐   add post to your favorites
    🗑️  to remove a message
    🔁   get another random post
    
    For search terms, see https://danbooru.donmai.us/wiki_pages/help:cheatsheet
    """
}


def get_data(command_name: str):
    url = short_urls.get(command_name)
    description = desc.get(command_name) or f"""
                Searches images from {url}
                
                Emojis 
                ⭐   add post to your favorites
                🗑️  to remove a message
                🔁   get another random post

                For search terms, see https://{url}/index.php?page=help&topic=cheatsheet
                """

    data_dict = dict(
        name=command_name,
        brief=f'Search images from {url}',
        description=description,
    )

    return data_dict


class PostCog(commands.Cog):
    @commands.command(**get_data('rule34'), aliases=['r34'])
    async def rule34(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await PostFactory.create_xml_post(ctx, tags, score)

    @commands.command(**get_data('xbooru'))
    async def xbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await PostFactory.create_xml_post(ctx, tags, score)

    @commands.command(**get_data('gelbooru'))
    async def gelbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str):
        await PostFactory.create_xml_post(ctx, tags, score)

    @commands.command(**get_data('tbib'))
    async def tbib(self, ctx: Context, *, tags: str):
        await PostFactory.create_tbib_post(ctx, tags)

    @commands.command(**get_data('danbooru'), aliases=['dbooru'])
    async def danbooru(self, ctx: Context, score: Optional[int] = 50, *, tags: str, ):
        await PostFactory.create_json_post(ctx, tags, score)

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
