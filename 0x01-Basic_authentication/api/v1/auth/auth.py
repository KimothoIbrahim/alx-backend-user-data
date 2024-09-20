#!/usr/bin/env python3
"""Module to Handle authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current User
        """
        return None
