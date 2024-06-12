from enum import StrEnum
from typing import Type, Any

from pydantic import BaseModel
from requests import request, Request as src_Request

from api.custom_response import CustomResponse
from other.logging import log_request, log_response
from other.model import convert_model


class MethodEnum(StrEnum):
    """Перечисление доступных методов запроса"""
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Request:
    """Класс для отправки API-запросов"""
    headers, params, data, files, json, token_cache = {}, {}, {}, {}, {}, {}

    def request(
            self,
            url: str,
            method: MethodEnum,
            headers: dict[str, Any] | None = None,
            data: dict | list | str | bytes | BaseModel | None = None,
            params: dict[str, Any] | None = None,
            timeout: int | float | None = None,
            json: dict | list | BaseModel | None = None,
            response_model: Type[BaseModel] | None = None,
            response_error_model: Type[BaseModel] | None = None,
            **kwargs,
    ) -> CustomResponse:
        """Отправить запрос и залогировать запрос и ответ

        Args:
            url: адрес
            method: HTTP-метод
            headers: заголовки, если есть
            data: тело запроса, если есть
            json: тело запроса в формате dict
            params: параметры запроса, если есть
            timeout: таймаут, который надо выждать прежде чем отправить запрос
            response_model: Схема ответа
            response_error_model: схема ответа для негативных сценариев
            **kwargs: кварги для метода преобразования объекта модели
        """
        if isinstance(data := data if data else self.data, BaseModel):
            data = convert_model(model=data, is_json=True, **kwargs)

        if isinstance(json := json if json else self.json, BaseModel):
            json = convert_model(model=json, **kwargs)

        log_request(
            request=src_Request(
                url=url,
                method=f'{method}',
                headers=headers if headers else self.headers,
                params=params if params else self.params,
                data=data if data else self.data,
                json=json if json else self.json
            ).prepare()
        )

        response = request(
            url=url,
            method=f'{method}',
            headers=headers if headers else self.headers,
            params=params if params else self.params,
            data=data if data else self.data,
            json=json if json else self.json,
            verify=False,
            timeout=timeout
        )
        log_response(response=response)

        return CustomResponse(
            response=response,
            response_model=response_model,
            response_error_model=response_error_model
        )
