import base64
import json
from pathlib import Path
from urllib.parse import urlencode
import requests
from keap.KeapToken import KeapToken
from keap.XML.XML import XML
from keap.settings import APISettings
from keap.storages import BaseStorage, JSONStorage


class Keap:
    rest_url = 'https://api.infusionsoft.com/crm/rest/v1/'
    authorize_url = 'https://signin.infusionsoft.com/app/oauth/authorize'
    access_token_url = 'https://api.infusionsoft.com/token'
    app_name: str = None
    storage: BaseStorage = None
    api_settings: APISettings
    xml_client = None

    def __init__(self, config: dict = None, config_file: Path = None):
        if config and config_file:
            raise ValueError("You can only load settings from one source")
        if config_file:
            with open(config_file, 'r') as f:
                config = json.load(f)
        self.api_settings = APISettings(config)
        if not self.api_settings.CLIENT_ID:
            raise Exception("Missing Client Id")
        if not self.api_settings.CLIENT_SECRET:
            raise Exception("Missing Client Secret")

        self.app_name = self.api_settings.APP_NAME

        self.storage = self.api_settings.STORAGE_CLASS()
        if isinstance(self.api_settings.STORAGE_CLASS(), JSONStorage):
            if not self.api_settings.JSON_STORAGE_PATH:
                raise Exception("JSON_STORAGE_PATH must be defined for JSONStorage")
            self.storage.storage_path = self.api_settings.JSON_STORAGE_PATH

        # self.XML = XML(self)

    @property
    def XML(self):
        if not self.xml_client:
            self.xml_client = XML(self)
        return self.xml_client

    @property
    def token(self) -> KeapToken:
        return self.storage.get_token(self.app_name)

    def save_token(self, token):
        self.storage.save_token(self.app_name, token)
        self.xml_client = XML(self)

    def get_authorization_url(self, state=''):
        data = {
            'client_id': self.api_settings.CLIENT_ID,
            'redirect_uri': self.api_settings.REDIRECT_URL,
            'response_type': 'code',
            'scope': 'full',
            'state': state
        }
        return self.authorize_url + "?" + urlencode(data)

    def request_access_token(self, code):
        data = {
            'client_id': self.api_settings.CLIENT_ID,
            'client_secret': self.api_settings.CLIENT_SECRET,
            'redirect_uri': self.api_settings.REDIRECT_URL,
            'code': code,
            'grant_type': 'authorization_code',
        }
        authorization_token_response = requests.post(self.access_token_url, data)
        token = KeapToken(**authorization_token_response.json())
        self.save_token(token)
        return self.token

    def refresh_access_token(self):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.token.refresh_token
        }
        auth_header = "Basic " + base64.b64encode(
            bytes(f"{self.api_settings.CLIENT_ID}:{self.api_settings.CLIENT_SECRET}", 'utf-8')
        ).decode()
        refresh_token_response = requests.post(self.access_token_url, data, headers={'Authorization': auth_header})
        # TODO: Make sure valid token is returned before setting and saving.
        token = KeapToken(**refresh_token_response.json())
        self.save_token(token)
        return self.token

    def change_app(self, app_name):
        self.app_name = app_name
        if not self.token.access_token:
            raise Exception(f"{app_name} does not have a token in storage, please authenticate")
        self.xml_client = XML(self)
