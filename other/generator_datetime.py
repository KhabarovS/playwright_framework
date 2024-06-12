from datetime import datetime, timedelta, date


class GeneratorDateTime:
    """ Класс с кастомным генератором даты и времени """

    def __init__(self, dt: datetime = datetime.now(), fmt: str = '%d.%m.%YT%H:%M:%S'):
        """

        Args:
            dt: пользовательская дата и время. По умолчанию текущая дата и время
            fmt: формат для преобразования в строку
        """
        self._dt = dt
        self._fmt = fmt

    @property
    def dt(self) -> datetime:
        """ Получить дату в виде datetime формат"""
        return self._dt

    def as_string(self) -> str:
        """ Получить дату в виде строки"""
        return self._dt.strftime(self._fmt)

    def quarter(self) -> int:
        """ Получить квартал текущей даты """
        return (self._dt.month - 1) // 3 + 1

    def set_datetime_with_offset(
            self,
            to_the_future: bool = True,
            utc: bool = False,
            working_day: bool = False,
            holiday: bool = False,
            seconds: int = 0,
            minutes: int = 0,
            hours: int = 0,
            days: int = 0,
            weeks: int = 0
    ):
        """ Изменить текущую дату и время на определенный сдвиг

        Args:
            to_the_future: флаг указывающий сдвиг в будущее;
            working_day: смещать дату на рабочий день;
            holiday: смещать дату на выходной день;
            seconds: количество секунд сдвига;
            minutes: количество минут сдвига;
            hours: количество часов сдвига;
            days: количество дней сдвига;
            weeks: количество недель сдвига;
            utc: флаг необходимости использования часового пояса UTC;
        """
        date_with_offset = datetime.utcnow() if utc else self._dt
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
        date_with_offset = date_with_offset + delta if to_the_future else date_with_offset - delta

        if working_day:
            number_of_day = date.isoweekday(date_with_offset)

            if number_of_day in (6, 7):
                date_with_offset += timedelta(days=(8 - number_of_day))

        if holiday:
            date_with_offset += timedelta(days=(6 - date.isoweekday(date_with_offset)))

        self._dt = date_with_offset
