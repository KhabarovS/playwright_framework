from typing import Type

from pydantic import BaseModel

from api.custom_request import MethodEnum
from api.custom_response import CustomResponse
from api.services.reqres_in.reqres_in import ReqresIn
from dto.unknown_dto import ResourceListResponseDto, ResourceSingleResponseDto


class ReqresUnknown(ReqresIn):
    """ Класс эндпоинта /unknown/   """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/unknown'

    def get_unknown_list(
            self,
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = ResourceListResponseDto,
    ) -> CustomResponse:
        """Получить список ресурсов

        Args:
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=MethodEnum.GET,
            url=self.url,
            request_model=req_model,
            response_model=res_model,
        )

    def get_single_unknown(
            self,
            resource_id: int,
            req_model: Type[BaseModel] | None = None,
            res_model: Type[BaseModel] | None = ResourceSingleResponseDto,
    ) -> CustomResponse:
        """Получить информацию о ресурсе

        Args:
            resource_id: идентификатор ресурса
            req_model: модель запроса
            res_model: модель ответа
        """
        return self.request(
            method=MethodEnum.GET,
            url=f'{self.url}/{resource_id}',
            request_model=req_model,
            response_model=res_model,
        )
