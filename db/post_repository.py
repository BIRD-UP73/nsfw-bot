import logging
from datetime import datetime
from typing import List

from discord import User

from db.model import session, Post as DBPost
from posts.data.post_data import Post
from posts.post_entry import PostEntry
from url.urls import URL


def get_favorites(user: User) -> List[PostEntry]:
    """
    Returns all favorites for a user

    :param user: the user
    :return: the favorites for the specified user
    """
    posts = session.query(DBPost).filter(DBPost.user_id == user.id).order_by(DBPost.saved_at.asc())

    logging.info(f'Fetched favorites, user={user}')

    return [PostEntry(URL.find(db_post.url), db_post.post_id, db_post.saved_at) for db_post in posts]


def remove_favorite(user: User, post: Post):
    """
    Removes a favorite from a user
    This will not succeed if the user is not stored in the database
    Or if the user did not have the favorite

    :param user: the user
    :param post: the post
    :return: True if removing succeeds, False if not
    """
    db_post = session.query(DBPost).get((user.id, post.post_id, post.board_url.short_url))

    session.delete(db_post)
    session.commit()
    logging.info(f'Removed favorite, user={user}, post_id={post.post_id}, url={post.board_url}')


def exists(user: User, post: Post) -> bool:
    """
    Checks whether a post exists for a given user

    :param user: the user
    :param post: the post
    :return: True if the post exists, False if not
    """
    db_post = session.query(DBPost).get((user.id, post.post_id, post.board_url.short_url))

    return db_post is not None


def store_favorite(user: User, post: Post) -> bool:
    """
    Stores a favorite for a user
    This might fail if the user already has the post as a favorite

    :param user: the user
    :param post: the post
    :return: True if storing the favorite succeeds, False if not
    """
    if post.is_error() or exists(user, post):
        return False

    db_post = DBPost(user_id=user.id, post_id=post.post_id, url=post.board_url.short_url, saved_at=datetime.now())
    session.add(db_post)
    session.commit()

    logging.info(f'Stored favorite, user={user}, post_id={post.post_id}, url={post.board_url}')
    return True
