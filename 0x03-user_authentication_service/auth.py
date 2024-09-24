#!/usr/bin/env python3
"""Auth module
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    """Hash a password
    """
    import bcrypt

    salt = bcrypt.gensalt()

    if password:
        return bcrypt.hashpw(password.encode('utf-8'), salt)


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