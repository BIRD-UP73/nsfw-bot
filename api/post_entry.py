from xml.etree import ElementTree

from api.json_api import JsonPostData, json_post_by_id
from api.post_data import PostData, PostError
from api.xml_api import XmlPostData, get_post_by_id
from util.url_util import short_to_long


class PostEntry:
    post_data: PostData

    def __init__(self, url: str, post_id: int):
        self.url = url
        self.post_id = post_id

    def fetch_post(self) -> PostData:
        if 'danbooru' in self.url:
            return self.get_json_post()
        return self.get_xml_post()

    def get_json_post(self) -> PostData:
        long_url = short_to_long(self.url)
        json_post = json_post_by_id(long_url, self.post_id)

        return JsonPostData(**json_post)

    def get_xml_post(self) -> PostData:
        long_url = short_to_long(self.url)
        resp_text = get_post_by_id(long_url, self.post_id)
        et_post = ElementTree.fromstring(resp_text)

        if len(et_post) == 0:
            return PostError('Could not find post.')

        return XmlPostData.from_xml(et_post[0], 1)

    def to_content(self) -> dict:
        self.post_data = self.fetch_post()
        return self.post_data.to_content()
