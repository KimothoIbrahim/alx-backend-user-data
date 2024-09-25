#!/usr/bin/env python3
"""Auth module
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password
    """

    salt = bcrypt.gensalt()

    if password:
        return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid():
    """str uid
    """
    import uuid
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """register users
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound as err:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """check login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
            return False
        except (NoResultFound, Exception) as err:
            return False
