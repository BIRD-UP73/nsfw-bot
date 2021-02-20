from typing import List

from discord import User

from api.post_data import PostData
from db.model import session, User as DBUser, Post as DBPost


def get_favorites(user: User) -> List[PostData]:
    """
    Returns all favorites for a user
    :param user: the user
    :return: the favorites for the specified user
    """
    db_user = session.query(DBUser).get(user.id)

    if not db_user:
        return []

    return [PostData.from_db_post(db_post) for db_post in db_user.posts]


def remove_favorite(user: User, post_data: PostData):
    """
    Removes a favorite from a user
    This will not succeed if the user is not stored in the database
    Or if the user did not have the favorite

    :param user: the user
    :param post_data: the post that might be a user's favorite
    :return: True if removing succeeds, False if not
    """
    db_user = session.query(DBUser).get(user.id)

    if not db_user:
        return False

    db_post = session.query(DBPost).get(post_data.file_url)

    if db_post in db_user.posts:
        db_user.posts.remove(db_post)
        session.commit()
        return True

    return False


def store_favorite(user: User, post_data: PostData):
    """
    Stores a favorite for a user
    This might fail if the user already has the post as a favorite

    :param user: the user
    :param post_data: the post data that should be stored
    :return: True if storing the favorite succeeds, False if not
    """
    db_user = session.query(DBUser).get(user.id)

    if not db_user:
        db_user = DBUser(id=user.id)
        session.add(db_user)

    db_post = session.query(DBPost).get(post_data.file_url)

    if not db_post:
        db_post = post_data.to_db_post()

    if db_post not in db_user.posts:
        db_user.posts.append(db_post)
        session.commit()
        return True

    return False
