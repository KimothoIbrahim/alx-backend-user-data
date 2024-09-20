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
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if path in excluded_paths or f'{path}/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current User
        """
        return None
