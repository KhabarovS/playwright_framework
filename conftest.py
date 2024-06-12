from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from allure import attach, attachment_type, step, title
from playwright.sync_api import sync_playwright, Browser
from playwright.sync_api._generated import Playwright as SyncPlaywright

from other.config import Config
from other.logging import create_logger, logger
from web.browser_factory import BrowserFactory


def pytest_addoption(parser: pytest.Parser):
    """Парсер для аргументов командной строки.

    Args:
        parser: Инстанс Parser.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер",
        choices=['chrome', 'firefox']
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Укажите параметр, если хотите запустить браузер в headless режиме"
    )

    parser.addoption(
        "--remote",
        action="store_true",
        help="Укажите параметр, если хотите запустить удаленный браузер"
    )

    parser.addoption(
        "--log_level",
        action='store',
        default='INFO',
        help='Уровень логгирования',
        choices=['DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    )

    parser.addoption(
        "--web_url",
        action='store',
        help='Базовый URL WEB-страниц'
    )


def pytest_configure(config: pytest.Config):
    """Положить параметры запуска в окружение

    Args: config: Config для доступа к значениям конфигурации, менеджеру плагинов и хукам плагинов
    """
    Config.log_level = config.getoption('--log_level')
    create_logger(log_level=Config.log_level, params=config.option)

    Config.is_headless = config.getoption('--headless')
    Config.is_remote = config.getoption('--remote')
    Config.browser_name = config.getoption('--browser')
    Config.web_url = config.getoption('--web_url')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo):  # noqa
    """Хук для сохранения скриншота при падении

    Args:
        item: выполненный тест
        call: объект с информацией о вызове функции

    Returns:

    """
    outcome = yield
    rep: TestReport = outcome.get_result()

    if (
            rep.when == 'call'
            and any(map(lambda x: x in item.fixturenames, ['browser', 'open_page']))
            and rep.failed
    ):
        try:
            logger.info(f'Сохранить скриншот при падении теста: {rep.nodeid}')
            attach(
                name=f'screenshot_{rep.nodeid}',
                body=Config.page.screenshot(full_page=True),
                attachment_type=attachment_type.PNG
            )
            logger.info('Скриншот успешно сохранен')
        except Exception:
            logger.warning('Не удалось сохранить скриншот')


@pytest.fixture(scope='session', params=[()])
@title('Инициализировать браузер с параметрами')
def browser(request: SubRequest) -> Browser:
    """Инициализировать экземпляр браузера

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
    """
    playwright: SyncPlaywright = sync_playwright().start()

    with step(f'Создать экземпляр браузера {Config.browser_name}, Remote={Config.is_remote}'):
        Config.browser = BrowserFactory.get_browser(
            playwright=playwright,
            browser_name=Config.browser_name,
            add_opts=[option for option in request.param],
            is_headless=Config.is_headless
        )

    yield Config.browser

    try:
        for context in Config.browser.contexts:
            context.close()

        Config.browser.close()
        playwright.stop()
        logger.info('Сессия браузера закрыта!')

    except TimeoutError:
        logger.warning('Сессия закрылась по таймауту!')
