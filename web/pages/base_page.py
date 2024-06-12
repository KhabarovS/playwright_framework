from allure import step
from playwright.sync_api import Browser, BrowserContext, Page, Locator as PlaywrightLocator

from other.config import Config
from other.logging import logger
from other.utils import get_seconds_time
from web import browser_config
from web.locator import Locator, format_locator
from playwright._impl._errors import TimeoutError


class BasePage:
    """ Базовый класс страницы для работы с элементами """

    def __init__(self, browser: Browser, context: BrowserContext | None = None):
        """

        Args:
            browser: экземпляр браузера
        """
        self._browser = browser
        self.url = Config.web_url
        self._context = context if context else self._browser.new_context(no_viewport=True)
        self._page = self._context.new_page()

        Config.page = self._page

    @property
    def browser(self) -> Browser:
        """ Получить экземпляр браузера """
        return self._browser

    @property
    def context(self) -> BrowserContext:
        """ Получить экземпляр контекста """
        return self._context

    @property
    def page(self) -> Page:
        """ Получить экземпляр контекста """
        return self._page

    @property
    def current_url(self) -> str:
        """ Получить текущий url """
        return self._page.url

    @step('Открыть url класса')
    def get(self):
        """ Перейти по ссылке класса """
        logger.info(f'Открываем страницу {self.url}')
        self._page.goto(self.url)
        self._page.wait_for_load_state()
        logger.success(f'Страница {self.url} открыта')

    @step('Открыть страницу по url')
    def open_page(self, url: str):
        """ Перейти по ссылке

        Args:
            url: ссылка
        """
        logger.info(f'Открываем страницу {url}')
        self._page.goto(url)
        self._page.wait_for_load_state()
        logger.success(f'Страница {url} url')

    @format_locator
    @step('Найти элемент по локатору')
    def find_element_by_locator(
            self,
            locator: Locator,
            timeout: float = browser_config.TIMEOUT,
            **kwargs
    ) -> PlaywrightLocator:
        """Ожидать присутствие элемента на странице

        Args:
            locator: локатор
            timeout: таймаут ожидания в миллисекундах
        """
        seconds = get_seconds_time(milliseconds=timeout)

        try:
            logger.info(f'Ожидаем присутствия  элемента с локатором {locator} в течение {seconds} секунд')

            pw_locator = self._page.locator(selector=locator.locator).first
            pw_locator.wait_for(state='attached', timeout=timeout)

            logger.success(f'Элемент {locator} найден')

            return pw_locator

        except TimeoutError as e:
            e.args += f'Элемент {locator} не найден в течение {seconds} секунд',
            raise e

    @format_locator
    @step('Найти элементы на странице по локатору')
    def find_elements_by_locator(self, locator: Locator, **kwargs) -> list[PlaywrightLocator]:
        """Найти список элементов на странице

        Args:
            locator: локатор
        """
        logger.info(f'Поиск локаторов {locator}')
        pw_locator = self._page.locator(selector=locator.locator).all()
        logger.success(f'Найдено {len(pw_locator)} элементов по локатору {locator}')

        return pw_locator

    @format_locator
    @step('Ожидать видимость элемента')
    def find_visible_element_by_locator(
            self,
            locator: Locator,
            timeout: float = browser_config.TIMEOUT,
            **kwargs
    ) -> PlaywrightLocator:
        """Ожидать присутствия элемента в DOM страницы и его видимости.

        Args:
            locator: Инстанс Locator;
            timeout: Количество миллисекунд до тайм-аута ожидания;
            **kwargs: Аргументы для форматирования локатора.
        """
        seconds = get_seconds_time(milliseconds=timeout)

        try:
            logger.info(f'Ожидаем видимый {locator} в течение {seconds} секунд')

            pw_locator = self._page.locator(selector=locator.locator).first
            pw_locator.wait_for(state='visible', timeout=timeout)

            logger.success('Элемент найден и виден!')

            return pw_locator

        except TimeoutError as e:
            logger.error(msg := f'Не удалось найти видимый {locator} в течение {seconds} секунд')
            e.args += f'\n{msg}',

            raise e

    @format_locator
    @step('Скролл страницы до элемента')
    def scroll_into_view_by_locator(
            self,
            locator: Locator,
            timeout: float = browser_config.TIMEOUT,
            **kwargs
    ) -> PlaywrightLocator:
        """Проскролить страницу до элемента

        Args:
            locator: локатор
            timeout: таймаут в миллсекундах
        """
        logger.info('Скролить страницу до элемента')

        pw_locator = self.find_element_by_locator(locator=locator, timeout=timeout)
        pw_locator.scroll_into_view_if_needed(timeout=timeout)

        logger.success('Страница прокручена до элемента')

        return pw_locator

    @format_locator
    @step('Кликнуть по элементу')
    def click_by_locator(
            self,
            locator: Locator,
            timeout: float = browser_config.TIMEOUT,
            **kwargs
    ) -> PlaywrightLocator:
        """Найти элемент и кликнуть по нему

        Args:
            locator: локатор
            timeout: таймаут в миллисекундах
        """
        try:
            logger.info(f'Клик по элементу {locator}')
            pw_locator = self.find_visible_element_by_locator(locator=locator, timeout=timeout)

            pw_locator.click(timeout=timeout)

            logger.success('Клик успешно выполнен')

            return pw_locator

        except TimeoutError as e:
            logger.error(msg := f'Не удалось кликнуть по элементу {locator}')
            e.args = msg,

            raise e

    @format_locator
    @step('Ввести значение в элемент по локатору')
    def send_keys_by_locator(
            self,
            locator: Locator,
            keys: str,
            timeout: float = browser_config.TIMEOUT,
            **kwargs
    ) -> PlaywrightLocator:
        """Найти элемент по локатору и ввести в него значение

        Args:
            locator: локатор
            keys: текст для ввода
            timeout: таймаут в миллисекундах
        """
        try:
            logger.info(f'Ввод значения в элемент {locator}')
            pw_locator = self.find_element_by_locator(locator=locator, timeout=timeout)
            pw_locator.fill(keys)

            logger.success('Значение успешно введено')

            return pw_locator

        except Exception as e:
            logger.error(msg := f'Не удалось ввести значение  {keys} в элемент {locator}')
            e.args = msg,

            raise e

    @format_locator
    @step('Очистить поле по локатору')
    def clear_by_locator(
            self,
            locator: Locator,
            timeout: float = browser_config.TIMEOUT,
            **kwargs
    ) -> PlaywrightLocator:
        """Очистить поле для ввода

        Args:
            locator: локатор
            timeout: таймаут в секундах
        """
        try:
            logger.info(f'Очистка элемента {locator}')

            pw_locator = self.find_element_by_locator(locator=locator, timeout=timeout)
            pw_locator.clear(timeout=timeout)

            logger.success(f'Элемент {locator} успешно очищен')

            return pw_locator

        except TimeoutError as e:
            logger.error(msg := f'Не удалось очистить элемент {locator}')
            e.args = msg,

            raise e

    @step('Открыть новую вкладку')
    def open_new_tab(self, page: type['BasePage']) -> 'BasePage':
        """Создать новую вкладку

        Args:
            page: предполагаемая страница
        """
        logger.info('Открыть новую вкладку')
        new_tab = page(self._browser, context=self._context)

        logger.success(f'Новая вкладка открыта со страницей {page.__class__.__name__}')

        return new_tab

    @step('Закрыть вкладку по url')
    def closed_tab_by_url(self, url: str) -> None:
        """Закрыть вкладку по открытому url

        Args:
            url: url вкладки
        """
        all_pages = self._context.pages
        logger.debug(f'Полученные страницы: {all_pages}')

        logger.info(f'Закрыть вкладку с {url=}')
        for page in all_pages:
            if url in page.url:
                page.close()
                break

        else:
            logger.warning(f'Вкладка с {url=} не найдена')

        logger.success(f'Вкладка с {url=} успешно закрыта')

    @step('Закрыть вкладку по индексу')
    def closed_tab_by_index(self, index: int) -> None:
        """Закрыть вкладку по индексу

        Args:
            index: индекс вкладки(нумерация с нуля)
        """
        all_pages = self._context.pages
        logger.debug(f'Полученные страницы: {all_pages}')

        logger.info(f'Закрыть вкладку с {index=}')

        if len(all_pages) >= index:
            raise IndexError('Индекс вкладки больше, чем фактическое число открытых вкладок')

        all_pages[index].close()

        logger.success(f'Вкладка с {index=} успешно закрыта')
