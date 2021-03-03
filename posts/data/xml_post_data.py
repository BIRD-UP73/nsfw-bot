from xml.etree import ElementTree

from discord import Embed

from posts.data.post_data import PostData


class XmlPostData(PostData):
    total_posts = 0

    def __init__(self, total_posts, **kwargs):
        super().__init__(**kwargs)
        self.total_posts = total_posts

    @classmethod
    def from_xml(cls, el: ElementTree, total_posts: int):
        file_url = el.get('file_url')

        data = dict(
            file_url=file_url,
            file_ext=file_url.split('.')[-1],
            created_at=el.get('created_at'),
            score=el.get('score'),
            source=el.get('source'),
            tags=el.get('tags'),
            id=el.get('id')
        )

        return cls(total_posts, **data)

    def to_embed(self) -> Embed:
        embed = super().to_embed()
        embed.description = f'Found {self.total_posts} images'
        return embed
