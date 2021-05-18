from discord import User

from posts.post_entry import PostEntry


class FavoriteEvent:
    def __init__(self, post_entry: PostEntry, user: User):
        self.post_entry: PostEntry = post_entry
        self.user: User = user
