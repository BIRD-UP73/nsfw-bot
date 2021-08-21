import logging
from typing import Union
from xml.etree import ElementTree

from discord import DMChannel, TextChannel

from posts.api.xml_api import send_request
from posts.data.post_data import NonExistentPost
from posts.data.xml_post_data import XmlPost
from posts.fetcher.post_fetcher import PostFetcher
from posts.paginator.paginator import Paginator
from posts.post_history import PostHistory
from url.urls import UrlEnum


class XmlPostFetcher(PostFetcher):
    def __init__(self, url: UrlEnum, paginator: Paginator):
        super().__init__(url, paginator)
        # self.max_count: Optional[int] = max_count

    def fetch_for_page(self, page: int, source: Union[DMChannel, TextChannel]):
        resp_text = send_request(self.url, 1, self.tags, page)
        posts = ElementTree.fromstring(resp_text)

        if len(posts) == 0:
            logging.warning(f'XML post not found, url={self.url}, tags={self.tags}, page={page}')
            self.post_data = NonExistentPost()
        else:
            self.post_data = XmlPost.from_xml(self.url, posts[0])

        PostHistory().add_to_history(source, self.post_data)
