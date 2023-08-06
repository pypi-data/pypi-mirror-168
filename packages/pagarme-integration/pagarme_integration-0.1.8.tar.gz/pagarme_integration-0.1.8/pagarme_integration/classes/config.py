from requests.auth import HTTPBasicAuth


class Config:
    __header = {
        "Accept": "application/json",
    }
    __url = "https://api.pagar.me/core/v5"

    @classmethod
    def set_auth(cls, key):
        cls.__auth = HTTPBasicAuth(key, "")

    @classmethod
    def get_header(cls):
        return cls.__header

    @classmethod
    def get_url(cls):
        return cls.__url

    @classmethod
    def get_auth(cls):
        return cls.__auth
