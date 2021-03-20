from xml.etree import ElementTree

from posts.data.post_data import PostData


class XmlPostData(PostData):
    @classmethod
    def from_xml(cls, el: ElementTree):
        file_url = el.get('file_url')

        attrs = dict(
            file_url=file_url,
            file_ext=file_url.split('.')[-1],
            created_at=el.get('created_at'),
            score=el.get('score'),
            source=el.get('source'),
            tags=el.get('tags'),
            id=el.get('id')
        )

        return cls(**attrs)
