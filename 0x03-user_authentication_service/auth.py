#!/usr/bin/env python3
"""Auth module
"""


def _hash_password(password: str) -> bytes:
    """Hash a password
    """
    import bcrypt

    salt = bcrypt.gensalt()

    if password:
        return bcrypt.hashpw(password.encode('utf-8'), salt)
