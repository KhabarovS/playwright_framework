from typing import Type

from pydantic import BaseModel

from api.custom_request import MethodEnum
from api.custom_response import CustomResponse
from api.services.reqres_in.reqres_in import ReqresIn
from dto.register_dto import RegisterResponse


class ReqresRegister(ReqresIn):
    """ Класс эндпоинта /register/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/register'

    def post_register(
            self,
            data: str | None = None,
            json: dict | None = None,
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = RegisterResponse
    ) -> CustomResponse:
        """ Отправить запрос на регистрацию

        Args:
            data: тело запроса
                email - почта пользователя
                password - пароль пользователя
            json: тело запроса
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=MethodEnum.POST,
            url=self.url,
            data=data,
            json=json,
            request_model=req_model,
            response_model=res_model
        )
