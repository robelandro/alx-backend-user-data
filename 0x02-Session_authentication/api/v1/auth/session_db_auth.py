#!/usr/bin/env python3
""" SessionDBAuth module """

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if session_id is None or type(session_id) is not str:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user_session = UserSession.search({'user_id': user_id})
        if len(user_session) == 0:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_id
        if 'created_at' not in user_session:
            return None
        created_at = user_session.get('created_at')
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None
        return user_id

    def destroy_session(self, request=None):
        """ Destroys the User Session / Logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        user_sessions = UserSession.search({'user_id': user_id})
        for user_session in user_sessions:
            user_session.remove()
        return True
