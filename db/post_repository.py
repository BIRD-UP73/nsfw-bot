from typing import List, Tuple

from discord import User

from db.model import session, Post as DBPost
from util.url_util import parse_url


def get_favorites(user: User) -> List[Tuple]:
    """
    Returns all favorites for a user
    :param user: the user
    :return: the favorites for the specified user
    """
    posts = session.query(DBPost).filter(DBPost.user_id == user.id)
    return [(db_post.url, db_post.post_id) for db_post in list(posts)]


def remove_favorite(user: User, url: str, post_id: int):
    """
    Removes a favorite from a user
    This will not succeed if the user is not stored in the database
    Or if the user did not have the favorite

    :param user: the user
    :param url: the post's url
    :param post_id: the post id
    :return: True if removing succeeds, False if not
    """
    parsed_url = parse_url(url)
    db_post = session.query(DBPost).get((user.id, post_id, parsed_url))

    session.delete(db_post)
    session.commit()


def exists(user: User, url: str, post_id: int):
    """
    Checks whether a post exists for a given user
    :param user: the user
    :param url: the post url
    :param post_id: the post
    :return: True if the post exist, False if not
    """
    parsed_url = parse_url(url)
    db_post = session.query(DBPost).get((user.id, post_id, parsed_url))

    return db_post is not None


def store_favorite(user: User, url: str, post_id: int):
    """
    Stores a favorite for a user
    This might fail if the user already has the post as a favorite

    :param user: the user
    :param url: the post url
    :param post_id: the post id
    :return: True if storing the favorite succeeds, False if not
    """
    parsed_url = parse_url(url)

    db_post = DBPost(user_id=user.id, post_id=post_id, url=parsed_url)
    session.add(db_post)
    session.commit()
