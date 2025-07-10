from datetime import datetime, timedelta
import secrets
from threading import Lock

class KeyManager():
    def __init__(self, previous_key=None, rotation_interval= timedelta(minutes=30)):
        self.active_key = self.generate_new_key()
        self.previous_key = previous_key
        self.last_rotation = datetime.now()
        self.rotation_interval = rotation_interval

    def generate_new_key(self):
        key = secrets.token_urlsafe(32)
        return key

    def rotate_key(self):
        self.previous_key = self.active_key
        self.active_key = self.generate_new_key()
        self.last_rotation = datetime.now()

    def get_active_key(self):
        return self.active_key

    def get_valid_keys(self):
        keys = []

        keys.append(self.active_key)

        if self.previous_key is not None:
            keys.append(self.previous_key)
        
        return keys

    def should_rotate(self):
        datetime.now()

        time_difference = datetime.now() - self.last_rotation

        if time_difference >= self.rotation_interval:
            return True
        else:
            return False

    
