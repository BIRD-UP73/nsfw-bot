from xml.etree import ElementTree

from posts.api.json_api import json_post_by_id
from posts.api.xml_api import get_post_by_id
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import PostData, NonExistentPost
from posts.data.xml_post_data import XmlPostData
from posts.fetcher.post_entry_key import PostEntryKey
from urls import danbooru
from util.url_util import short_to_long


class PostKeyFetcher:
    @staticmethod
    def fetch(post_key: PostEntryKey) -> PostData:
        if post_key.url in danbooru:
            return PostKeyFetcher.get_json_post(post_key)

        return PostKeyFetcher.get_xml_post(post_key)

    @staticmethod
    def get_json_post(post_key: PostEntryKey) -> PostData:
        long_url = short_to_long(post_key.url)
        json_post = json_post_by_id(long_url, post_key.post_id)

        if json_post.get('success') is False:
            return NonExistentPost()

        return JsonPostData(**json_post)

    @staticmethod
    def get_xml_post(post_key: PostEntryKey) -> PostData:
        long_url = short_to_long(post_key.url)
        resp_text = get_post_by_id(long_url, post_key.post_id)
        et_post = ElementTree.fromstring(resp_text)

        count = et_post.get('count')

        if count is None or int(count) == 0:
            return NonExistentPost()

        return XmlPostData.from_xml(et_post[0])
