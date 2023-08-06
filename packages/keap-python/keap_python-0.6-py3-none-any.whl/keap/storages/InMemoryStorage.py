import json
from json import JSONDecodeError
from pathlib import Path

from keap.KeapToken import KeapToken
from keap.storages import BaseStorage


class InMemoryStorage(BaseStorage):
    tokens: dict = {}

    def __init__(self):
        super().__init__()

    def get_token(self, app) -> KeapToken:
        try:
            if app in self.tokens:
                return self.tokens[app]
        except Exception as e:
            pass
        return KeapToken()

    def save_token(self, app: str, token: KeapToken) -> bool:
        try:
            self.tokens[app] = token
            return True
        except Exception as e:
            pass
        return False
