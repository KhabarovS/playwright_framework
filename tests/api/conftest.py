from typing import Optional, Type

from _pytest.fixtures import SubRequest
from pydantic import BaseModel
from pytest import fixture


@fixture
def get_request_to_reqres(request: SubRequest) -> tuple[int, Optional[Type[BaseModel]]]:
    """Отправить запрос с аргументами и преобразовать в экземпляр модели или в None

    Args:
        request: параметры фикстуры:
            method - Метод запроса
            kwargs - кварги для отправки запроса
            model - модель для парса ответа
    """
    method, kwargs, model = request.param

    response = method(**kwargs)

    body = model(**response.json()) if response.text else None

    return response.status_code, body
