""" Модуль с функциями логгера """
import sys
from argparse import Namespace
from json import dumps, loads

from allure import attach, attachment_type, step
from loguru import logger
from requests import PreparedRequest, Response

from other.config import Config
from other.utils import get_curl


class InvalidLogLevel(Exception):
    """Исключение при попытке задать неподдерживаемый уровень логирования"""

    def __init__(self, log_level: str, available_log_levels: str):
        self.log_level, self.available_log_levels = log_level, available_log_levels

    def __str__(self):
        return f'Указан недопустимый уровень логирования: "{self.log_level}". ' \
               f'Пожалуйста, укажите один из следующих уровней: {self.available_log_levels}'


def create_logger(log_level: str, params: Namespace) -> None:
    """ Создать логер и установить уровень логирования

    Args:
        log_level: уровень логирования
        params: параметры запуска проекта
    """
    try:
        logger.remove()

        if getattr(params, 'xmlpath', None):  # если формируется xml, то выводить лог без цветового выделения
            logger.add(
                sink=sys.stdout,
                level=log_level,
                format='\n{time:HH:mm:ss.SSS} | {level} | {message}'
            )
        else:
            logger.add(
                sink=sys.stdout,
                format=(
                    '\n<fg #ff7e00>{time:HH:mm:ss.SSS}</fg #ff7e00> | '
                    '<level>{level}</level> | '
                    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | '
                    '<level>{message}</level>'
                ),
                level=log_level,
                colorize=True
            )

    except ValueError:
        logger.error(f'Ошибка при установке уровня логирования {log_level=}')
        raise InvalidLogLevel(
            log_level=log_level,
            available_log_levels=getattr(logger, '_core').levels.keys()
        )


def set_log_level(log_level: str):
    """ Установить уровень логирования

    Args:
        log_level: уровень логирования
    """
    if log_level:
        try:
            logger.level(name=log_level)

        except ValueError as e:
            e.args = 'Не правильный уровень логирования',

        logger.info(f'Установлен уровень логирования: {log_level}')

    else:
        logger.info(f'Установлен уровень логирования: {Config.log_level}')


def attach_body(body: str | bytes):
    """Прикрепить в allure тело запроса

    Args:
        body: Тело запроса
    """
    try:
        body = body if type(body) == str else body.decode()
        attach(
            body=dumps(obj=loads(body), indent=2),
            name='BODY',
            attachment_type=attachment_type.JSON
        )

    except Exception:
        attach(body=body, name='BODY', attachment_type=attachment_type.TEXT)


def log_request(request: PreparedRequest, is_compressed: bool = False, is_insecure: bool = False):
    """Залогировать запрос

    Args:
        request: запрос
        is_compressed: параметр, позволяющий сформировать curl для запроса сжатого ответа
        is_insecure: параметр, позволяющий сформировать curl для "небезопасного" SSL соединения и передачи данных
    """
    curl = None
    msg = f'HTTP-Method: <blue><normal>{request.method}</normal></blue>\n' \
          f'\t URL:     <blue><normal>{request.url}</normal></blue>\n' \
          f'\t Headers: <blue><normal>{request.headers}</normal></blue>\n'

    if 'boundary' not in request.headers and request.method != 'GET':
        msg += f'\t Body:    <blue><normal>{request.body}</normal></blue>\n'

    if 'boundary' not in request.headers:
        curl = get_curl(request=request, is_compressed=is_compressed, is_insecure=is_insecure)
        msg += f'\t CURL:    <blue><normal>{curl}</normal></blue>'

    try:
        logger.opt(colors=True).info(msg)

    except ValueError:
        logger.opt(colors=False).info(msg.replace('<blue><normal>', '').replace('</normal></blue>', ''))

    with step(f'Запрос: [{request.method}] {request.url}'):
        attach(
            body=dumps(dict(request.headers), indent=2),
            name='HEADERS',
            attachment_type=attachment_type.JSON
        )
        attach_body(body=request.body)

        if curl:
            attach(body=curl, name='CURL', attachment_type=attachment_type.TEXT)


@logger.catch()
def log_response(response: Response):
    """Залогировать ответ

    Args:
        response: ответ
    """
    color = {
        1: 'light-blue',
        2: 'green',
        3: 'yellow',
        4: 'red',
        5: 'red'
    }.get(response.status_code // 100, "y")

    try:
        logger.opt(colors=True).info(
            f'Code: <{color}><n>{response.status_code}</n></{color}>\n'
            f'\t Headers: <{color}><n>{response.headers}</n></{color}>\n'
            f'\t Body:    <{color}><n>{response.text}</n></{color}>'
        )

        with step(f'Ответ: [{response.status_code}] {response.url}'):
            attach(
                body=dumps(dict(response.headers), indent=2),
                name='HEADERS',
                attachment_type=attachment_type.JSON
            )
            attach_body(body=response.content)

    except ValueError:
        logger.opt(colors=True).info(
            f'Code: <{color}><normal>{response.status_code}</normal></{color}>\n'
            f'\t Headers: <{color}><normal>{response.headers}</normal></{color}>\n'
        )
        logger.info(f'Body: {response.text}')
