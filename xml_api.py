import random
import xml.etree.ElementTree as et
from typing import Union
from xml.dom.minidom import Element

import requests
from dateutil import parser
from discord import Embed, Reaction, User
from discord.ext.commands import Context


POST_LIMIT = 2500
MAX_POSTS_PER_PAGE = 100

img_fmts = ['png', 'jpg', 'jpeg', 'tiff', 'gif']


class Post:
    def __init__(self, ctx: Context, url: str, tags: str, el: Element, total_posts=0):
        self.ctx = ctx
        self.score = int(el.get('score'))
        self.file_url = el.get('file_url')
        self.sample_url = el.get('sample_url')
        self.created_at = parser.parse(el.get('created_at'))
        self.source = el.get('source')
        self.format = self.file_url.split('.')[-1]
        self.tags = tags
        self.url = url
        self.total_posts = total_posts
        self.msg = None

    def fill_data(self, el: Element):
        self.score = int(el.get('score'))
        self.file_url = el.get('file_url')
        self.sample_url = el.get('sample_url')
        self.created_at = parser.parse(el.get('created_at'))
        self.source = el.get('source')
        self.format = self.file_url.split('.')[-1]

    def to_content(self) -> Union[Embed, str]:
        embed = Embed()
        embed.description = f'Found {self.total_posts} images'
        embed.timestamp = self.created_at

        embed.add_field(name='Score', value=str(self.score))
        embed.add_field(name='URL', value=self.file_url)

        if self.format in img_fmts:
            embed.set_image(url=self.file_url)
        else:
            return self.file_url

        embed.set_footer(text=self.tags)
        return embed

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
            _, xml_post = get_xml_post(self.tags, self.url)

            self.fill_data(xml_post)
            content = self.to_content()

            if isinstance(content, str):
                await self.msg.edit(content=self.to_content())
            else:
                await self.msg.edit(embed=content)

            await self.msg.remove_reaction(reaction.emoji, user)


def get_xml_post(tags, url) -> Element:
    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, 0, url)
    posts = et.fromstring(resp_text)
    total_posts = int(posts.get('count') or 0)

    max_posts_to_search = min(total_posts, POST_LIMIT)
    max_pages = max_posts_to_search // MAX_POSTS_PER_PAGE

    if max_posts_to_search == 0:
        return 0, None

    random_page = random.randint(0, max_pages)

    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, random_page, url)
    posts = et.fromstring(resp_text)

    random.shuffle(posts)
    return total_posts, posts[0]


async def get_rule_34(ctx: Context, tags: str, score, url: str):
    if 'score:>=' not in tags:
        tags += f' score:>{score}'

    total_posts, xml_post = get_xml_post(tags, url)

    if xml_post is None:
        await ctx.send('No images found')
    else:
        post = Post(ctx, url, tags, xml_post, total_posts=total_posts)
        await post.send_message()


def send_request(limit: int, tags: str, page: int, url: str) -> str:
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'limit': limit,
        'pid': page,
        'tags': tags
    }

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.text
