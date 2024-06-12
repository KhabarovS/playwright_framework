"""Конфигурация с параметрами запуска"""
from pathlib import Path

from playwright.sync_api import Browser, Page


class Config:
    """Абстрактный класс с параметрами запуска. Заполняется при старте проекта"""
    browser: Browser
    page: Page
    browser_name: str
    is_remote: bool = False
    is_headless: bool = False
    stand: str
    web_url: str
    log_level = "INFO"
    test_data_dir = Path('test_data').absolute()
    timeout = 30
