from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from dto.generic import ReqresDto


class RegisterResponse(ReqresDto):
    """ Схема регистрации пользователя """
    id_: Optional[StrictInt] = Field(None, by_alias='id', validation_alias='id')
    token: Optional[StrictStr] = None
    error: Optional[StrictStr] = None
