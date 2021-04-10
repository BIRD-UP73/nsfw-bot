from discord import User

from db import post_repository
from posts.data.post_data import Post
from util.url_util import parse_url


def add_favorite(user: User, post_data: Post):
    """
    Adds a post to a user's favorites
    :param user: the user
    :param post_data: the entry with the post
    :return: whether adding the favorite succeeded
    """
    url = parse_url(post_data.file_url)

    if post_data.is_error() or post_repository.exists(user, url, post_data.post_id):
        return False

    post_repository.store_favorite(user, url, post_data.post_id)
    return True
