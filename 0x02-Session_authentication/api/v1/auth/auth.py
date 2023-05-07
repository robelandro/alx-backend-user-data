#!/usr/bin/env python3
"""
a module to manage the API authentication.
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """a class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        a method that returns False - path and excluded_paths will not be used.
        """

        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        for i in excluded_paths:
            if i[-1] == '*':
                if i[:-1] in path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        a method that returns None - request will not be used.
        """

        if request is None or request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        a method that returns None - request will not be used.
        """
        return None

    def session_cookie(self, request=None):
        """
        a method that returns None - request will not be used.
        """
        if request is None:
            return None

        SESSION_NAME = getenv("SESSION_NAME")

        if SESSION_NAME is None:
            return None

        session_id = request.cookies.get(SESSION_NAME)

        return session_id
