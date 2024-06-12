"""Методы валидации тел ответа по схеме Pydantic"""
from json import dumps
from typing import Type

from allure import attach, step
from pydantic import BaseModel, ValidationError
from pytest import fail

from other.logging import logger


@logger.catch
@step('Валидация тела ответа по схеме')
def is_valid(model: Type[BaseModel], response: dict):
    """Валидировать тело ответа по схеме

    Args:
        model: Схема тела ответа
        response: JSON, dict, list ответа
    """
    with step('Проверка тела по схеме'):
        _model, _response = model.model_json_schema(), dumps(response)
        attach(_response, name='Тело ответа')
        attach(str(_model), name='Модель')

        try:
            model.model_validate(response)

        except ValidationError as e:
            logger.error(
                f'Ошибка валидации тела ответа!'
                f'\nОшибка:\n{e}\n'
                f'\nМодель: {_model}'
                f'\nТело:   {_response}'
            )
            fail(reason=str(e))


def convert_model(model: BaseModel, is_json: bool = False, **kwargs) -> list | dict | str:
    """Преобразование модели в объект для отправки в request: str, dict, list

    Args:
        model: объект модели;
        is_json:    True - результат возвращается в формате json;
                    False - результат возвращается в dict/list
        **kwargs: кварги для метода преобразования
    """
    result = model.model_dump_json(**kwargs) if is_json else model.model_dump(**kwargs)

    if 'root' in result:
        result = result['root']

    is_list = True if isinstance(result, list) else False

    logger.debug(
        'Преобразование модели: \n'
        f'\tМодель: {model}\n'
        f'\tПреобразование: {"json" if is_json else "list" if is_list else "dict"}\n'
        f'\tРезультат: {result}'
    )

    return result
