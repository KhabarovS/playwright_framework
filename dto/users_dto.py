from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, StrictInt, StrictStr

from dto.generic import ReqresDto


class UsersDto(ReqresDto):
    """ Схема пользователя """
    id_: StrictInt = Field(alias='id')
    email: EmailStr
    first_name: StrictStr
    last_name: StrictStr
    avatar: StrictStr


class SupportDto(ReqresDto):
    """ Схема поддержки """
    url: StrictStr
    text: StrictStr


class UserResponseDto(ReqresDto):
    """ Схема ответа одиночного пользователя """
    data: Optional[UsersDto] = None
    support: Optional[SupportDto] = None


class UsersListResponseDto(ReqresDto):
    """ Схема ответа со списком пользователей """
    page: StrictInt
    per_page: StrictInt
    total: StrictInt
    data: Optional[list[UsersDto]] = Field(...)


class RequestUserDto(ReqresDto):
    """ Схема запроса создания/обновления пользователя """
    name: StrictStr
    job: StrictStr


class UpdateUserDto(RequestUserDto):
    """ Схема ответа обновления пользователя """
    updatedAt: datetime


class CreateUserDto(RequestUserDto):
    """ Схема ответа создания пользователя """
    createdAt: datetime
    id_: StrictStr = Field(alias='id')
