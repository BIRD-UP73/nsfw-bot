from datetime import datetime
from xml.etree import ElementTree

from posts.api.json_api import json_post_by_id
from posts.api.xml_api import get_post_by_id
from posts.data.json_post_data import JsonPostData
from posts.data.post_data import PostData, NonExistentPost
from posts.data.xml_post_data import XmlPostData
from util.url_util import short_to_long


class PostEntry:
    def __init__(self, url: str, post_id: int, saved_at: datetime, post_data: PostData = None):
        self.url: str = url
        self.post_id: int = post_id
        self.saved_at: datetime = saved_at
        self.post_data = post_data

    def fetch_post(self) -> PostData:
        if self.post_data:
            return self.post_data

        if 'danbooru' in self.url:
            self.post_data = self.get_json_post()
        else:
            self.post_data = self.get_xml_post()

        return self.post_data

    def get_json_post(self) -> PostData:
        long_url = short_to_long(self.url)
        json_post = json_post_by_id(long_url, self.post_id)

        if json_post.get('success') is False:
            return NonExistentPost()

        return JsonPostData(**json_post)

    def get_xml_post(self) -> PostData:
        long_url = short_to_long(self.url)
        resp_text = get_post_by_id(long_url, self.post_id)
        et_post = ElementTree.fromstring(resp_text)

        count = et_post.get('count')

        if count is None or int(count) == 0:
            return NonExistentPost()

        return XmlPostData.from_xml(et_post[0])
