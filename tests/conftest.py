from typing import Annotated

from _pytest.fixtures import SubRequest
from allure import step, title
from playwright.sync_api import Browser
from pytest import fixture

from other.logging import logger


@fixture(scope='session')
@title('Открыть страницу')
def open_page(request: SubRequest, browser: Annotated[Browser, fixture]):
    """Открыть браузер и страницу.

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры;
        browser: экземпляр браузера.
    """
    if not (param := getattr(request, 'param', None)):
        logger.error(msg := f'В фикстуру не переданы обязательные параметры через indirect: page')
        raise RuntimeError(msg)

    with step(msg := f'Открыть страницу {param}'):
        logger.info(msg)
        page = param(browser=browser)
        page.get()

    yield page
