import logging

from xml.etree import ElementTree

from posts.api.json_api import json_post_by_id
from posts.api.xml_api import get_post_by_id
from posts.data.hypnohub_post_data import HypnohubPost
from posts.data.json_post_data import JsonPost
from posts.data.post_data import Post, NonExistentPost
from posts.data.xml_post_data import XmlPost
from posts.post_entry_key import PostEntryKey
from url.urls import Danbooru, URL, Hypnohub


class PostKeyFetcher:
    @staticmethod
    def fetch(post_key: PostEntryKey) -> Post:
        if post_key.url == Danbooru:
            return PostKeyFetcher.get_json_post(post_key)

        return PostKeyFetcher.get_xml_post(post_key)

    @staticmethod
    def get_json_post(post_key: PostEntryKey) -> Post:
        json_post = json_post_by_id(post_key.url.long_url, post_key.post_id)

        if json_post.get('success') is False:
            logging.warning(f'JSON post not found, url={post_key.url}, id={post_key.post_id}')
            return NonExistentPost()

        return JsonPost(post_key.url, **json_post)

    @staticmethod
    def get_xml_post(post_key: PostEntryKey) -> Post:
        resp_text = get_post_by_id(post_key.url, post_key.post_id)
        et_post = ElementTree.fromstring(resp_text)

        count = et_post.get('count')

        if count is None or int(count) == 0:
            logging.warning(f'XML post not found, url={post_key.url}, id={post_key.post_id}')
            return NonExistentPost()

        return PostKeyFetcher.parse_post(post_key.url, et_post[0])

    @staticmethod
    def parse_post(url: URL, et_post: ElementTree):
        if url == Hypnohub:
            return HypnohubPost.from_xml(url, et_post)

        return XmlPost.from_xml(url, et_post)
