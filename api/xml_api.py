import random
import xml.etree.ElementTree as et
from xml.dom.minidom import Element

import requests
from discord.ext.commands import Context, CommandError

from api.post import Post, PostData

POST_LIMIT = 2500
MAX_POSTS_PER_PAGE = 100


class XmlPost(Post):
    def fetch_post(self):
        total_posts, xml_post = get_xml_post(self.tags, self.url)

        if total_posts == 0:
            raise CommandError(f'No images found for {self.tags}')

        self.post_data = PostData.from_xml(xml_post, total_posts)

        hist_cog = self.bot.get_cog('PostHist')
        hist_cog.add_post(self.post_data.file_url)


def get_xml_post(tags: str, url: str) -> Element:
    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, 0, url)
    posts = et.fromstring(resp_text)

    total_posts = int(posts.get('count'))
    max_posts_to_search = min(total_posts, POST_LIMIT)
    max_pages = max_posts_to_search // MAX_POSTS_PER_PAGE

    if max_posts_to_search == 0:
        return 0, None

    random_page = random.randint(0, max_pages)

    resp_text = send_request(MAX_POSTS_PER_PAGE, tags, random_page, url)
    posts = et.fromstring(resp_text)

    random.shuffle(posts)
    return total_posts, posts[0]


async def show_post(ctx: Context, tags: str, score, url: str):
    if 'score:>=' not in tags:
        tags += f' score:>{score}'

    post = XmlPost(ctx.bot, url, tags)
    await post.create_message(ctx)


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
