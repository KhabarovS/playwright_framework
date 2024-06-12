import sys
from pathlib import Path

from playwright.sync_api import Browser
from playwright.sync_api._generated import Playwright as SyncPlaywright

from other.logging import logger
from web.browser_config import ChromeConfig


class BrowserFactory:
    """Класс для создания экземпляров различных браузеров"""

    @staticmethod
    def __create_chrome_browser(
            playwright: SyncPlaywright,
            is_headless: bool,
            add_opts: list[str] | None = None
    ) -> Browser:
        """Создать экземпляр Chrome браузера

        Args:
            add_opts: дополнительные опции
        """
        return playwright.chromium.launch(headless=is_headless, args=ChromeConfig.default_options + add_opts)

    @staticmethod
    def get_browser(
            playwright: SyncPlaywright,
            browser_name: str,
            is_headless: bool,
            add_opts: list[str] | None = None,
    ) -> Browser:
        """Получить экземпляр браузера

        Args:
            playwright: объект playwright
            is_headless: запуск в headless режиме
            browser_name: название браузера
            add_opts: дополнительные опции
        """
        logger.info(
            f'Переданы настройки браузера:\n'
            f'\tБраузер:       \t{browser_name}\n'
            f'\tДоп. аргументы:\t{add_opts}\n'
            f'\tis_headless:   \t{is_headless}'
        )
        return {
            'chrome': BrowserFactory.__create_chrome_browser
        }[browser_name](playwright=playwright, add_opts=add_opts, is_headless=is_headless)
