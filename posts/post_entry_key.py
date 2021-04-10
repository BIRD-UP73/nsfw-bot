
class PostEntryKey:
    def __init__(self, post_id: int, url: str):
        self.post_id: int = post_id
        self.url = url

    def __eq__(self, other):
        if isinstance(other, PostEntryKey):
            return self.url == other.url and self.post_id == other.post_id
        return False

    def __hash__(self):
        return hash((self.post_id, self.url))
