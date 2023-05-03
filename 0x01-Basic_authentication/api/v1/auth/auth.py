#!/usr/bin/env python3
"""
a module to manage the API authentication.
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """a class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        a method that returns False - path and excluded_paths will not be used.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        a method that returns None - request will not be used.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        a method that returns None - request will not be used.
        """
        return None
