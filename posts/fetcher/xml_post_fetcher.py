from typing import Union
from xml.etree import ElementTree

from discord import DMChannel, TextChannel

from posts.api.xml_api import send_request
from posts.data.post_data import NonExistentPost
from posts.data.xml_post_data import XmlPost
from posts.fetcher.post_fetcher import PostFetcher
from posts.post_history import PostHistory

max_posts = 200000


class XmlPostFetcher(PostFetcher):
    def fetch_count(self) -> int:
        # Fetch 0 posts to just get the post count
        resp_text = send_request(self.url, 0, self.tags, 0)
        posts = ElementTree.fromstring(resp_text)

        if text_count := posts.get('count'):
            return min(int(text_count), max_posts)

        return 0

    def fetch_for_page(self, page, source: Union[DMChannel, TextChannel]):
        resp_text = send_request(self.url, 1, self.tags, page)
        posts = ElementTree.fromstring(resp_text)

        if len(posts) == 0:
            self.post_data = NonExistentPost()
        else:
            self.post_data = XmlPost.from_xml(posts[0])

        PostHistory().add_to_history(source, self.post_data)
