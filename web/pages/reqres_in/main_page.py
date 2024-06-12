from enum import Enum

from allure import step
from playwright.sync_api import Browser

from other.config import Config
from web.locator import Locator
from web.pages.base_page import BasePage


class RequestEnum(Enum):
    """Перечисление доступных методов на UI"""
    LIST_USERS = 'users'
    SINGLE_USERS = 'users-single'
    SINGLE_USER_NOT_FOUND = 'users-single-not-found'
    LIST_RESOURCE = 'unknown'
    SINGLE_RESOURCE = 'unknown-single'
    SINGLE_RESOURCE_NOT_FOUND = 'unknown-single-not-found'
    CREATE_USER = 'post'
    PUT_UPDATE_USER = 'put'
    PATCH_UPDATE_USER = 'patch'
    DELETE_USER = 'delete'
    REGISTER_SUCCESSFUL = 'register-successful'
    REGISTER_UNSUCCESSFUL = 'register-unsuccessful'
    LOGIN_SUCCESSFUL = 'login-successful'
    LOGIN_UNSUCCESSFUL = 'register-unsuccessful'
    DELAY = 'delay'


class MainPage(BasePage):
    """Класс основной страницы сервиса Reqres.in"""
    GET_METHODS = Locator(name='Поле отправки метода {text}', locator='//li[@data-id="{text}"]//a')
    RESPONSE_STATUS_CODE = Locator(name='Статус код ответа',locator='//*[contains(@class,"response-code")]')
    RESPONSE_BODY = Locator(name='Тело ответа', locator='//*[@data-key="output-response"]')
    LOAD_SPINNER_HIDE = Locator(name='Скрытый спиннер загрузки', locator='//*[@data-key="spinner" and @hidden="true"]')

    def __init__(self, browser: Browser):
        """

        Args:
            browser: экземпляр Browser.
        """
        super().__init__(browser=browser)
        self.url = Config.web_url

    @step('Кликнуть на запрос для отправки на UI')
    def click_by_request(self, name_request: RequestEnum):
        """Кликнуть элемент для отправки запроса на UI

        Args:
            name_request: наименование метода на UI
        """
        with step(f'Клик на запрос {name_request.value}'):
            self.click_by_locator(locator=self.GET_METHODS, text=name_request.value)
