from json import dumps
from typing import Any

from allure import attach, attachment_type, step
from jsonpath_rw_ext import parse
from requests import PreparedRequest

from other.logging import logger


@logger.catch
def get_curl(
        request: PreparedRequest,
        is_compressed: bool = False,
        is_insecure: bool = False,
        is_breaks: bool = False
) -> str:
    """Получить curl запроса

    Args:
        request: запрос
        is_compressed: параметр позволяющий сформировать curl для запроса сжатого ответа;
        is_insecure: параметр явно позволяет сформировать curl для "небезопасного" SSL соединения и передачи данных;
        is_breaks: вернуть курл с переносами
    """
    sep = ' ' if not is_breaks else '\n'
    body = request.body

    curl_attrs = [
        f'curl -X {request.method}',
        sep.join([f'-H "{k}: {v}"' for k, v in request.headers.items()]),
        f'-d "{body.decode("latin-1") if isinstance(body, bytes) else body}"' if body else '',
        '--compressed ' if is_compressed else '',
        '--insecure ' if is_insecure else '',
        request.url
    ]

    return sep.join([attr for attr in curl_attrs if attr])


@step('Поиск значения в словаре')
def find_value_from_json(json: dict[str, Any], jp_expr: str) -> Any:
    """ Найти значение в json по JPExpression

    Args:
        json: json, в котором надо найти значение
        jp_expr: путь до значения
    """
    found = [match.value for match in parse(jp_expr).find(json)]

    if len(found) > 1:
        result = found

    elif len(found) == 1:
        result = found[0]

    else:
        raise ValueError(f'Значение по пути {jp_expr} не найдено')

    attach(body=str(result), name='РЕЗУЛЬТАТ', attachment_type=attachment_type.TEXT)
    logger.info(
        f'Поиск значения из JSON\n'
        f'\tПуть:\t\t{jp_expr}\n'
        f'\tJSON:\t\t{dumps(json)}\n'
        f'\tЗначение:\t{result}\n'
        f'\tТип:\t\t{type(result)}'
    )
    return result


def get_seconds_time(milliseconds: int | float) -> int:
    """Преобразовать миллисекунды в секунды

    Args:
        milliseconds: время в миллисекундах
    """
    return int(milliseconds / 1000)
