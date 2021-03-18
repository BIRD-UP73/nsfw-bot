from discord import User

from db import post_repository
from posts.data.post_entry import PostEntry


def add_favorite(user: User, entry: PostEntry):
    post_data = entry.post_data

    if post_data.is_error() or post_repository.exists(user, entry.url, post_data.post_id):
        return

    post_repository.store_favorite(user, entry.url, post_data.post_id)
