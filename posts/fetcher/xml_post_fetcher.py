import random

from typing import Union
from xml.etree import ElementTree

from discord import DMChannel, TextChannel

from posts.api.xml_api import send_request
from posts.data.post_data import NonExistentPost
from posts.data.xml_post_data import XmlPostData
from posts.fetcher.post_fetcher import PostFetcher
from posts.history import PostHistory


class XmlPostFetcher(PostFetcher):
    def random_page(self, source: Union[DMChannel, TextChannel]):
        page = random.randint(0, self.post_count)
        self.fetch_for_page(page, source)

    def next_page(self, source: Union[DMChannel, TextChannel]):
        page = self.paginator.next_page()
        self.fetch_for_page(page, source)

    def previous_page(self, source: Union[DMChannel, TextChannel]):
        page = self.paginator.previous_page()
        self.fetch_for_page(page, source)

    def fetch_count(self):
        # Fetch 0 posts to just get the post count
        resp_text = send_request(self.url, 0, self.tags, 0)
        posts = ElementTree.fromstring(resp_text)

        if text_count := posts.get('count'):
            self.paginator.post_count = int(text_count)

    def fetch_for_page(self, page, source: Union[DMChannel, TextChannel]):
        resp_text = send_request(self.url, 1, self.tags, page)
        posts = ElementTree.fromstring(resp_text)

        if len(posts) == 0:
            self.post_data = NonExistentPost()
        else:
            self.post_data = XmlPostData.from_xml(posts[0])

        PostHistory().add_to_history(source, self.post_data)
