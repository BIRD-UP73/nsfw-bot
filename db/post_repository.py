from typing import List

from discord import User

from api.api_db_wrapper import PostEntry
from db.model import session, User as DBUser, Post as DBPost
from util.url_util import parse_url


def get_favorites(user: User) -> List[PostEntry]:
    """
    Returns all favorites for a user
    :param user: the user
    :return: the favorites for the specified user
    """
    db_user = session.query(DBUser).get(user.id)

    if not db_user:
        return []

    return [PostEntry(db_post.url, db_post.id) for db_post in db_user.posts]


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
    db_user = session.query(DBUser).get(user.id)

    if not db_user:
        return False

    parsed_url = parse_url(url)
    db_post = session.query(DBPost).get((post_id, parsed_url))

    if db_post in db_user.posts:
        db_user.posts.remove(db_post)
        session.commit()
        return True

    return False


def store_favorite(user: User, url: str, post_id: int):
    """
    Stores a favorite for a user
    This might fail if the user already has the post as a favorite

    :param user: the user
    :param url: the post url
    :param post_id: the post id
    :return: True if storing the favorite succeeds, False if not
    """
    db_user = session.query(DBUser).get(user.id)

    if not db_user:
        db_user = DBUser(id=user.id)
        session.add(db_user)

    parsed_url = parse_url(url)

    db_post = session.query(DBPost).get((post_id, parsed_url))

    if not db_post:
        db_post = DBPost(id=post_id, url=parsed_url)

    if db_post not in db_user.posts:
        db_user.posts.append(db_post)
        session.commit()
        return True

    return False
