"""Модуль содержит конфиги для браузеров"""

TIMEOUT = 15000


class ChromeConfig:
    """Класс для хранения конфигурации Chrome драйвера."""
    default_options = [
        '--window-size=1920,1080',
        '--ignore-certificate-errors',
        '--disable-gpu',
        '--no-sandbox',
        '--lang=ru-RU',
    ]