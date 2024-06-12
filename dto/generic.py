from pydantic import BaseModel


class ReqresDto(BaseModel):
    """Базовый класс DTO сервиса Reqres.in"""

    class Config:
        use_enum_values = True
        populate_by_name = True

    def model_dump(self, *args, **kwargs):
        """ Перегрузка метода .dict с аргументами по умолчанию """
        params = {'by_alias': True} | dict(**kwargs)
        return super().model_dump(*args, **params)

    def model_dump_json(self, *args, **kwargs):
        """ Перегрузка метода .json с аргументами по умолчанию """
        params = {'by_alias': True} | dict(**kwargs)
        return super().model_dump_json(*args, **params)
