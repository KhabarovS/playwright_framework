from typing import Any, Self

from allure import step
from pydantic import BaseModel
from requests import Response
from requests.cookies import RequestsCookieJar
from requests.structures import CaseInsensitiveDict
from requests.utils import dict_from_cookiejar

from other.logging import logger
from other import model

ERROR_SUCCESS_MSG = 'Поле "success" отлично от {result}'
ERROR_STATUS_CUSTOM_MSG = 'Код статуса ответа {code} не совпадает с ожидаемым: {exp}'


class CustomResponse:
    """ Класс, расширяющий стандартный Response, поддержкой работы с моделями """

    __slots__ = ['response', 'response_model', 'response_error_model', '_response_body']

    def __init__(
            self,
            response: Response,
            response_model: type[BaseModel] | None = None,
            response_error_model: type[BaseModel] | None = None
    ):
        """

        Args:
            response: объект ответа, получаем из запроса через self.request;
            response_model: основная модель ответа, передается в методе запроса;
            response_error_model: модель ответа для негативных сценариев, передается в методе запроса.
        """
        self.response = response
        self._response_body: dict[str, Any] | None = None
        self.response_model = response_model
        self.response_error_model = response_error_model

    @property
    def status_code(self) -> int:
        """Вернуть код ответа"""

        logger.debug('Вызов метода status_code из объекта Response')
        return self.response.status_code

    @property
    def headers(self) -> CaseInsensitiveDict[str]:
        """Вернуть заголовки ответов"""

        logger.debug('Вызов метода headers из объекта Response')
        return self.response.headers

    @property
    def content(self) -> bytes:
        """Вернуть тело в байт-строке"""

        logger.debug('Вызов метода content из объекта Response')
        return self.response.content

    @property
    def text(self) -> str:
        """Вернуть тело в юникод строке"""

        logger.debug('Вызов метода text из объекта Response')
        return self.response.text

    @property
    def links(self) -> dict[str, Any]:
        """Вернуть хедеры link ответа в виде словаря"""

        logger.debug('Вызов метода links из объекта Response')
        return self.response.links

    @property
    def cookies(self) -> RequestsCookieJar:
        """Вернуть cookies ответа в виде RequestsCookieJar"""

        logger.debug('Вызов метода cookies из объекта Response')
        return self.response.cookies

    @property
    def cookies_as_dict(self) -> dict[str, Any]:
        """Вернуть cookies ответа в виде словаря"""

        logger.debug('Получить куки в виде словаря')
        result = dict_from_cookiejar(self.cookies)
        logger.success(f'Результат преобразования куков в словарь: {result}')

        return result

    @step('Вызвать исключение при неуспешном статус коде')
    def raise_for_status(self) -> Self:
        """Вызвать HTTPError ошибку клиента, если 400 <= статус код < 500
        или ошибку сервера, если 500 <= статус код < 600
        """

        logger.debug('Вызов метода raise_for_status из объекта Response')
        self.response.raise_for_status()

        return self

    @step('Получить тело ответа в виде словаря или списка')
    def json(self, **kwargs) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Вернуть весь ответ как dict/list

        Args:
            **kwargs: кварги для парса json.
        """

        logger.debug('Получить тело ответа в виде объекта python')

        if self._response_body is None:
            logger.debug('Тело не записано внутри экземпляра. Парс тела из ответа Response')

            self._response_body = self.response.json(**kwargs)

            logger.debug('Результат: {}. Тело записано в экземпляр', self._response_body)

        else:
            logger.debug('Тело уже записано внутри экземпляра. Возвращаем тело из экземпляра')

        return self._response_body

    @step('Получить значение поля success')
    def success(self) -> bool | None:
        """Получить success из ответа"""

        result: bool | None = None

        if body := self.json():

            if isinstance(body, dict):
                result = body.get('success')
                logger.debug('Получаем значение из ключа success. Полученное значение {}', result)

            else:
                logger.warning(
                    'Тело ответа не является словарем. Невозможно получить success! Тип тела ответа: {}', type(body)
                )
        else:
            logger.warning('Отсутствует тело ответа. Невозможно получить success!')

        return result

    @step('Преобразовать ответ в dto')
    def dto(self, is_error_model: bool = False) -> BaseModel:
        """Вернуть ответ как data transfer object

        Args:
            is_error_model: вернуть dto по модели для позитивных или негативных сценариев.
        """

        model_ = self.response_error_model if is_error_model else self.response_model

        if not model_:
            raise AttributeError(f'{"" if is_error_model else "Негативная "}Модель не задана!')

        if not self.json():
            raise AttributeError('Тело ответа отсутствует!')

        result = model_(**self._response_body)

        logger.debug('Тело ответа успешно преобразовано в dto. Результат: {}', result)

        return result

    @step('Проверить статус кода ответа')
    def __base_check_expected_status_code(self, expected_code: int, exception: type[Exception] | None = None):
        """Проверить статус код

        Args:
            expected_code: ожидаемый статус код;
            exception: вызов исключения, вместо ассерта.
        """

        msg = ERROR_STATUS_CUSTOM_MSG.format(code=self.status_code, exp=expected_code)

        if exception:
            logger.debug('Выполнение проверки статус кодов с вызовом исключения')

            if self.status_code != expected_code:
                raise exception(msg)

        logger.debug('Выполнение проверки статус кодов с вызовом ассерта')

        assert self.status_code == expected_code, msg

        logger.success('Статус код успешно проверен!')

    @step('Проверить(assert) статус кода ответа')
    def assert_status_code(self, expected_code: int = 200) -> Self:
        """Проверить статус код с ожидаемым значением

        Args:
            expected_code: ожидаемый статус код.
        """
        self.__base_check_expected_status_code(expected_code=expected_code)

        return self

    @step('Проверить(exception) статус кода ответа')
    def check_status_code(self, expected_code: int = 200, exception: type[Exception] = ValueError) -> Self:
        """Проверить статус код с ожидаемым значением, иначе вызов исключения

        Args:
            expected_code: ожидаемый статус код;
            exception: объект исключения.
        """
        self.__base_check_expected_status_code(expected_code=expected_code, exception=exception)

        return self

    def assert_model_valid(self, expected_model: type[BaseModel] | None = None, is_error_model: bool = False):
        """Валидировать схему ответа

        Args:
            expected_model: ожидаемая модель;
            is_error_model: проверять ответ по схеме для позитивных или негативных сценариев.
        """

        logger.debug('Выполнение валидации схемы модели с телом ответа')

        if (body_ := self.json()) is None:
            raise AttributeError('Тело ответа отсутствует.')

        inst_model = self.response_error_model if is_error_model else self.response_model

        model_ = expected_model if expected_model else inst_model

        if model_ is None:
            raise AttributeError(f'Отсутствует {"негативная " if is_error_model else ""}модель для валидации!')

        model.is_valid(model=model_, response=body_)

        logger.success('Тело ответа успешно проверено по схеме!')
