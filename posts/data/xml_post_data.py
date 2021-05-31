from xml.etree import ElementTree

from posts.data.post_data import Post
from url.urls import URL


class XmlPost(Post):
    @classmethod
    def from_xml(cls, board_url: URL, el: ElementTree):
        file_url = el.get('file_url')

        return Post.from_dict(
            board_url=board_url,
            created_at=el.get('created_at'),
            file_url=file_url,
            file_ext=file_url.split('.')[-1],
            id=el.get('id'),
            score=el.get('score'),
            source=el.get('source'),
            tags=el.get('tags')
        )
