from discord.ext.commands import Context

from posts.fetcher.xml_post_fetcher import XmlPostFetcher
from posts.post.post_message import PostMessage
from util import util


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    fetcher = XmlPostFetcher(url, tags)
    await PostMessage(fetcher, ctx).create_message()
