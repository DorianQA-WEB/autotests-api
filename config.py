from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, HttpUrl, FilePath, DirectoryPath
from typing import Self



class HTTPClient(BaseModel):
    """
    Настройки HTTP-клиента.

    Атрибуты:
        url (HttpUrl): Базовый URL для подключения к сервису.
        timeout (float): Таймаут ожидания ответа от сервера в секундах.
    """
    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        """
        Возвращает базовый URL как строку.

        Используется для удобного доступа к URL без необходимости преобразования.

        Возвращает:
            str: Адрес сервера в виде строки.
        """
        return str(self.url)


class TestDateConfig(BaseModel):
    """
    Конфигурация путей к тестовым данным.

    Атрибуты:
        image_png_file (FilePath): Путь к тестовому PNG-изображению, используемому в сценариях.
                                   Должен указывать на существующий файл.
    """
    image_png_file: FilePath


class Settings(BaseSettings):
    """
    Основной класс конфигурации приложения.

    Содержит все настройки, загружаемые из переменных окружения и .env-файла.
    Поддерживает вложенную структуру через разделитель точку (например, `test_data.image_png_file`).

    Атрибуты:
        test_data (TestDateConfig): Настройки путей к тестовым данным.
        http_client (HTTPClient): Настройки HTTP-клиента для взаимодействия с API.
        allure_results_dir (DirectoryPath): Путь к директории для сохранения результатов Allure.
                                           По умолчанию — './allure-results'.

    Методы:
        initialize() -> Self: Создаёт экземпляр настроек, гарантируя, что директория
                           для результатов Allure существует (создаёт её при необходимости).
    """
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    test_data: TestDateConfig
    http_client: HTTPClient
    allure_results_dir: DirectoryPath = DirectoryPath("allure-results")


    @classmethod
    def initialize(cls) -> Self:
        """
        Инициализирует настройки и обеспечивает наличие директории для отчётов Allure.

        Создаёт директорию './allure-results', если она не существует.

        Возвращает:
            Self: Экземпляр класса Settings с инициализированными значениями.
        """
        allure_results_dir = DirectoryPath("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)

        return Settings(allure_results_dir=allure_results_dir)

# Инициализация глобального объекта настроек
settings = Settings.initialize()

# Отладочный вывод всех параметров конфигурации
print('\n'.join([f'{key}={value}'for key, value in settings.model_dump().items()]))

