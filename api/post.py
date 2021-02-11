from datetime import datetime
from xml.dom.minidom import Element

from dateutil import parser
from discord import Reaction, User, Embed
from discord.ext.commands import Context, CommandError, Bot

import util


class PostData:
    artist_tag = ''
    character_tag = ''
    created_at: datetime = None
    file_ext = ''
    file_url = ''
    score = ''
    source = ''
    total_posts = 0

    @staticmethod
    def from_xml(el: Element, total_posts=0):
        post = PostData()

        if 'loli' in el.get('tags'):
            raise CommandError('No loli allowed')

        post.created_at = parser.parse(el.get('created_at'))

        file_url = el.get('file_url')

        post.file_ext = file_url.split('.')[-1]

        post.file_url = file_url
        post.score = el.get('score')
        post.source = el.get('source')
        post.total_posts = total_posts

        return post

    @staticmethod
    def from_json(json_dict: dict):
        if 'loli' in json_dict.get('tag_string'):
            raise CommandError('Bro, u just requested loli. U are going to bird down')

        post = PostData()

        post.artist_tag = json_dict.get('tag_string_artist')
        post.character_tag = json_dict.get('tag_string_character')
        post.created_at = json_dict.get('created_at')
        post.file_ext = json_dict.get('file_ext')
        post.file_url = json_dict.get('file_url')
        post.score = json_dict.get('score')
        post.source = json_dict.get('source')

        return post

    def to_content(self):
        if not util.is_image(self.file_ext):
            return {'embed': None, 'content': self.file_url}

        embed = Embed()

        if self.total_posts:
            embed.description = f'Found {self.total_posts} images'
        if self.created_at:
            embed.timestamp = parser.parse(str(self.created_at))

        if self.score:
            embed.add_field(name='Score', value=self.score)
        if self.character_tag and len(self.character_tag) < 1024:
            embed.add_field(name='Characters', value=self.character_tag)
        if self.artist_tag and len(self.artist_tag) < 1024:
            embed.add_field(name='Characters', value=self.character_tag)
        if self.source:
            embed.add_field(name='Source', value=self.source)

        if self.file_url:
            embed.set_image(url=self.file_url)

        return {'embed': embed, 'content': None}


class Post:
    def __init__(self, bot: Bot, url: str, tags: str):
        self.bot = bot
        self.url = url
        self.tags = tags
        self.msg = None
        self.post_data = None

    async def create_message(self, ctx: Context):
        self.fetch_post()

        content = self.post_data.to_content()
        self.msg = await ctx.send(**content)

        self.bot.add_listener(self.on_reaction_add)
        await self.msg.add_reaction('🗑️')
        await self.msg.add_reaction('🔁')

    def fetch_post(self) -> dict:
        """
        Abstract method to fetch a post
        Should override `self.post_data`
        """
        raise NotImplementedError('You cannot call Post directly and your class should implement fetch_post()')

    async def on_reaction_add(self, reaction: Reaction, user: User):
        if reaction.message.id != self.msg.id or user == self.bot.user:
            return
        if reaction.emoji == '🗑️':
            await self.msg.delete()
            self.bot.remove_listener(self.on_reaction_add)
            return

        if reaction.emoji == '🔁':
            self.fetch_post()
            await self.msg.edit(**self.post_data.to_content())

        await self.msg.remove_reaction(reaction.emoji, user)
