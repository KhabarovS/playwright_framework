from typing import Any, Type

from pydantic import BaseModel

from api.custom_request import MethodEnum
from api.custom_response import CustomResponse
from api.services.reqres_in.reqres_in import ReqresIn
from dto.users_dto import CreateUserDto, UserResponseDto, UsersListResponseDto, UpdateUserDto


class ReqresUsers(ReqresIn):
    """ Класс эндпоинта /users/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/users'

    def get_users(
            self,
            params: dict[str, Any],
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = UsersListResponseDto,
    ) -> CustomResponse:
        """ Получить информацию о пользователях

        Args:
            params: Параметры запроса:
                page - номер страницы
                delay - таймаут ожидания перед получением тела
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=MethodEnum.GET,
            url=self.url,
            params=params,
            request_model=req_model,
            response_model=res_model,
        )

    def get_single_user(
            self,
            user_id: int,
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = UserResponseDto
    ) -> CustomResponse:
        """ Получить информацию о пользователе

        Args:
            user_id: идентификатор пользователя
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=MethodEnum.GET,
            url=f'{self.url}/{user_id}',
            request_model=req_model,
            response_model=res_model,
        )

    def create_user(
            self, data: str | None = None,
            json: dict | None = None,
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = CreateUserDto,
    ) -> CustomResponse:
        """Создать пользователя

        Args:
            data: тело запроса в формате str
                name - имя пользователя
                job - должность
            json: тело запроса в формате dict
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=MethodEnum.POST,
            url=self.url,
            data=data,
            json=json,
            request_model=req_model,
            response_model=res_model,
        )

    def update_user(
            self,
            method: MethodEnum,
            user_id: int,
            data: str | None = None,
            json: dict | None = None,
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = UpdateUserDto,
    ) -> CustomResponse:
        """Обновить пользователя

        Args:
            method: PUT или PATCH
            user_id: идентификатор пользователя
            data: тело запроса в формате str
                name - имя пользователя
                job - должность
            json: тело запроса в формате dict
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=method,
            url=f'{self.url}/{user_id}',
            data=data,
            json=json,
            request_model=req_model,
            response_model=res_model,
        )

    def delete_user(self, user_id: int) -> CustomResponse:
        """Удалить пользователя

        Args:
            user_id: идентификатор пользователя
        """
        return self.request(method=MethodEnum.DELETE, url=f'{self.url}/{user_id}')
