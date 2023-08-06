import json
from json import JSONDecodeError

from keap import KeapToken


class BaseStorage:
    app: str = None

    def __init__(self):
        pass

    def get_token(self, app) -> KeapToken:
        raise NotImplementedError()

    def save_token(self, app: str, token: KeapToken) -> bool:
        raise NotImplementedError()
