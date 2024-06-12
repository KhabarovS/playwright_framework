from typing import Optional

from pydantic import Field, StrictStr

from dto.generic import ReqresDto


class LoginResponse(ReqresDto):
    """ Схема авторизации пользователя """
    token: Optional[StrictStr] = Field(None)
    error: Optional[StrictStr] = Field(None)
