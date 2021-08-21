from url.urls import UrlEnum


class PostEntryKey:
    def __init__(self, post_id: int, url: UrlEnum):
        self.post_id: int = post_id
        self.url: UrlEnum = url

    def __eq__(self, other):
        return isinstance(other, PostEntryKey) and self.url == other.url and self.post_id == other.post_id

    def __hash__(self):
        return hash((self.post_id, self.url))
