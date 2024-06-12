"""Модуль с классом и декоратором для работы с локаторами"""
from re import findall
from typing import Callable

from other.logging import logger


def format_locator(function: Callable) -> Callable:
    """Декоратор для форматирования локатора

    Args:
        function: декорируемая функция
    """
    def wrapper(*args, **kwargs):
        """Обертка над методом

        Args:
            *args: прочие арги
            **kwargs: прочие кварги
        """
        logger.debug(
            'Переданные значения:\n'
            f'\tArgs:\t{args}\n'
            f'\tKwargs:\t{kwargs}\n'
        )

        if kwargs:
            loc_before_format = kwargs['locator']
            kwargs['locator'] = kwargs['locator'](**kwargs)

            if loc_before_format.locator != kwargs['locator'].locator:
                logger.info(
                    f'Формат локатора перед методом {function.__name__}\n'
                    f'\tБыло:\t{loc_before_format}\n'
                    f'\tСтало:\t{kwargs["locator"]}'
                )

        return function(*args, **kwargs)

    return wrapper


class Locator:
    """ Класс локатора """
    name: str
    locator: str

    def __init__(self, name: str, locator: str):
        """

        Args:
            name: имя локатора
            locator: локатор
        """
        self.name = name
        self.locator = locator

    def __add__(self, other) -> str:
        return self.locator[1] + other

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name=}, {self.locator=})'

    def __str__(self) -> str:
        return f'Элемент "{self.name}" с локатором "{self.locator}"'

    def __call__(self, **kwargs):
        try:
            return Locator(
                name=self.name.format(**kwargs),
                locator=self.locator.format(**kwargs)
            )
        except KeyError as e:
            pattern = r'\{([A-Za-z_0-9]*)\}'

            kwargs_name = findall(pattern=pattern, string=self.name)
            kwargs_locator = findall(pattern=pattern, string=self.locator[1])

            missing_kwargs = ', '.join([k for k in {*kwargs_name, *kwargs_locator} if k not in kwargs])

            logger.error(f'Не переданы значения для форматирования {self}\n\tОтсутствуют значения: {missing_kwargs}')

            e.args = f'Отсутствуют значения [ {missing_kwargs} ] для локатора {self}'

            raise e
