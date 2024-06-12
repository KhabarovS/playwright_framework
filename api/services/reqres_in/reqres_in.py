from api.custom_request import Request
from other.config import Config


class ReqresIn(Request):
    """ Класс бизнес-сервиса Reqres.in"""

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.url = f'{Config.web_url}/api'
