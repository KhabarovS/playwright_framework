from typing import Type

from pydantic import BaseModel

from api.custom_request import MethodEnum
from api.custom_response import CustomResponse
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresLogin(ReqresIn):
    """ Класс эндпоинта /login/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/login'

    def post_login(
            self,
            data: str | None = None,
            json: dict | None = None,
            request_model: Type[BaseModel] | None = None,
            response_model: Type[BaseModel] | None = None,
    ) -> CustomResponse:
        """ Отправить запрос на авторизацию

        Args:
            data: тело запроса
                email - почта пользователя
                password - пароль пользователя
            json: тело запроса
            request_model: модель запроса
            response_model: модель ответа
        """
        return self.request(
            method=MethodEnum.POST,
            url=self.url,
            data=data,
            json=json,
            request_model=request_model,
            response_model=response_model
        )
