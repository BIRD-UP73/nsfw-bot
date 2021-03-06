from discord.ext.commands import Context, CommandError

from posts.api.json_api import send_json_request
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import PostData, PostHasDisallowedTags
from posts.post.post import AbstractPost
from util import util

danbooru_url = 'https://danbooru.donmai.us/posts.json'


class JsonPost(AbstractPost):
    def fetch_post(self) -> PostData:
        """
        Fetches a post from a site with a json-based API
        Will throw an error if no posts are found (nothing else to fetch)
        Will show an error embed if the post contains disallowed tags

        Also adds post to history

        :return: the fetched post
        """
        resp_json = send_json_request(danbooru_url, self.tags)

        if len(resp_json) == 0:
            raise CommandError(f'No posts found for {self.tags}')

        post_data = JsonPostData(**resp_json[0])

        if post_data.has_disallowed_tags():
            return PostHasDisallowedTags()

        self.update_hist(post_data)
        return post_data


async def show_post(ctx: Context, tags: str, score: int):
    if len(tags.split(' ')) < 2:
        tags = util.parse_tags(tags, score)

    post = JsonPost(ctx, danbooru_url, tags)
    await post.create_message()
