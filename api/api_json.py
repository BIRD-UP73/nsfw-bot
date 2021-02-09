from typing import Union

from dateutil import parser
import requests
from discord import Embed, Reaction, User
from discord.ext.commands import Context

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPost:
    def __init__(self, ctx: Context, search_tag: str, url: str, **kwargs):
        self.ctx = ctx
        self.search_tag = search_tag
        self.url = url
        self.score = kwargs.get('score')
        self.created_at = parser.parse(kwargs.get('created_at'))
        self.file_url = kwargs.get('file_url')
        self.source = kwargs.get('source')
        self.artist_tag = kwargs.get('tag_string_artist')
        self.character_tag = kwargs.get('tag_string_character')
        self.msg = None

    def fill_data(self, **kwargs):
        self.score = kwargs.get('score')
        self.created_at = parser.parse(kwargs.get('created_at'))
        self.file_url = kwargs.get('file_url')
        self.source = kwargs.get('source')
        self.artist_tag = kwargs.get('tag_string_artist')
        self.character_tag = kwargs.get('tag_string_character')

    def to_content(self) -> Union[Embed, str]:
        embed = Embed()

        embed.set_image(url=self.file_url)

        if self.score:
            embed.add_field(name='Score', value=self.score)
        if self.artist_tag:
            embed.add_field(name='Artist', value=self.artist_tag)
        if self.character_tag:
            embed.add_field(name='Characters', value=self.character_tag)

        embed.set_footer(text=self.search_tag)

        if self.created_at:
            embed.timestamp = self.created_at

        return embed

    @property
    def image_format(self):
        if len(self.file_url) < 4:
            return ''
        return self.file_url[-4:]

    async def send_message(self):
        content = self.to_content()

        if isinstance(content, str):
            self.msg = await self.ctx.send(self.to_content())
        else:
            self.msg = await self.ctx.send(embed=self.to_content())

        await self.msg.add_reaction('🗑️')
        await self.msg.add_reaction('🔁')
        self.ctx.bot.add_listener(self.on_reaction_add)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        if reaction.message.id != self.msg.id or user == self.ctx.bot.user:
            return
        if reaction.emoji == '🗑️':
            await self.msg.delete()
            self.ctx.bot.remove_listener(self.on_reaction_add)
        elif reaction.emoji == '🔁':
            json_post = send_request(self.url, self.search_tag, random=True)
            self.fill_data(**json_post[0])

            content = self.to_content()

            if isinstance(content, str):
                await self.msg.edit(content=self.to_content(), embed=None)
            else:
                await self.msg.edit(content='', embed=content)

        await self.msg.remove_reaction(reaction.emoji, user)


async def get_posts(ctx: Context, tags: str, score: int):
    if 'score:>' not in tags and len(tags.split(' ')) < 2:
        tags += f' score:>={score}'

    resp_json = send_request(danbooru_url, tags)

    if len(resp_json) == 0:
        await ctx.send('No images found')

    post = JsonPost(ctx, tags, danbooru_url, **resp_json[0])
    await post.send_message()


def send_request(url, tags, random=True):
    params = {
        'limit': '1',
        'random': random,
        'tags': tags
    }

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.json()
