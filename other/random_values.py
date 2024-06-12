from enum import Enum
from random import randint
from string import ascii_lowercase, digits

from allure import step
from mimesis import Person, Locale
from mimesis.random import Random

from other.logging import logger

msg = 'ГЕНЕРАТОР {gen}.\nРЕЗУЛЬТАТ: {result}'


class NameEnum(Enum):
    """ Перечисление возможных имен"""
    FULL_NAME = 'full_name'
    LAST_NAME = 'last_name'
    FIRST_NAME = 'first_name'


@step('Генератор. Получить случайное число')
def get_random_number(start: int = 1, end: int = 999999, length: int | None = None) -> int:
    """ Получить случайное число в заданном диапазоне или заданной длины

    Args:
        start: начало диапазона;
        end: конец диапазона;
        length: длина числа.
    """
    result = randint(10 ** (length - 1), (10 ** length) - 1) if length else randint(start, end)
    logger.info(msg.format(gen='случайного числа', result=result))

    return result


@step('Генератор. Получить случайную строку')
def get_random_string(length: int = 10):
    """ Получить случайную строку

    Args:
        length: длина строки
    """
    result = Random()._generate_string(
        str_seq=f'абвгдеёжзийклмнопрстуфхцчшщьыъэюя{ascii_lowercase}{digits}',
        length=length
    )
    logger.info(msg.format(gen='cлучайной строки', result=result))

    return result


def get_random_name(name: NameEnum = NameEnum.FULL_NAME) -> str:
    """Получить случайное имя

    Args:
        name: тип имени(полное имя, имя или фамилия)
    """
    result = getattr(Person(Locale.EN), name.value)()

    logger.info(msg.format(gen='случайного имени', result=result))

    return result


def get_random_job() -> str:
    """ Получить случайную работу"""
    result = Person(Locale.EN).occupation()

    logger.info(msg.format(gen='случайной работы', result=result))

    return result


def get_random_email(domains: tuple[str] = ('mail.ru', 'gmail.com', 'yandex.ru')) -> str:
    """ Получить случайный e-mail

    Args:
        domains: набор доменов
    """
    result = Person(locale=Locale.RU).email(domains=domains)

    logger.info(msg.format(gen='случайной почты', result=result))

    return result
