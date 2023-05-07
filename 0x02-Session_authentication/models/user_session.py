#!/user/bin/env python3
"""UserSession module"""

from models.base import Base


class UserSession(Base):
    """UserSession class"""
    def __init__(self, *args: list, **kwargs: dict):
        """Constructor"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.session_id = kwargs.get('session_id', "")

    def to_json(self, _=None):
        """to_json method"""
        json_dict = super().to_json()
        json_dict['user_id'] = self.user_id
        json_dict['session_id'] = self.session_id
        return json_dict
