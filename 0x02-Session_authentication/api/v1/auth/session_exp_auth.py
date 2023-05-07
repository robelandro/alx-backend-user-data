#!/usr/bin/env python3
"""
Session Authentication exp module
"""

from api.v1.auth.session_auth import SessionAuth
from models.user import User
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Exp Auth class
    """

    def __init__(self):
        """Constructor
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user_id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None or type(session_id) is not str:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            return None
        created_at = session_dictionary.get('created_at')
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None
        return session_dictionary.get('user_id')
