from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from dto.generic import ReqresDto
from dto.users_dto import SupportDto


class ResourceDto(ReqresDto):
    """ Схема объекта ресурса """
    id_: StrictInt = Field(alias='id')
    name: StrictStr
    year: StrictInt
    color: StrictStr = Field(pattern=r'^#[A-Fa-f0-9]{6}$')
    pantone_value: StrictStr


class ResourceSingleResponseDto(ReqresDto):
    """ Схема ответа с одиночным объектом ресурса """
    data: Optional[ResourceDto] = None
    support: Optional[SupportDto] = None


class ResourceListResponseDto(ReqresDto):
    """ Схема получения списка ресурсов """
    page: StrictInt
    per_page: StrictInt
    total: StrictInt
    total_pages: StrictInt
    data: list[ResourceDto]
    support: SupportDto
