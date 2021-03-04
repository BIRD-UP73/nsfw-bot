from discord.ext.commands import Context, CommandError

from posts.data.xml_post_data import XmlPostData
from posts.post.post import AbstractPost
from posts.data.post_data import PostHasDisallowedTags
from posts.api.xml_api import get_xml_post
from util import util


class XmlPost(AbstractPost):
    def __init__(self, ctx: Context, url: str, tags: str):
        super().__init__(ctx, url, tags)

    def fetch_post(self):
        total_posts, xml_post = get_xml_post(self.tags, self.url)

        if total_posts == 0:
            raise CommandError(f'No posts found for {self.tags}')

        post_data = XmlPostData.from_xml(xml_post, total_posts)
        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data


async def show_post(ctx: Context, tags: str, score: int, url: str, skip_score=False):
    if not skip_score:
        tags = util.parse_tags(tags, score)

    post = XmlPost(ctx, url, tags)
    await post.create_message()
