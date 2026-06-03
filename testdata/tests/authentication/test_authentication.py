"""
Интеграционные тесты для API аутентификации: вход (login), валидация ответа и JSON-схемы.

Этот модуль содержит тесты, проверяющие корректность эндпоинта `/api/v1/authentication/login`:
- Успешный вход пользователя с правильными учетными данными.
- Валидация статус-кода (200 OK).
- Проверка структуры ответа через Pydantic-схему и явную валидацию JSON-схемы.

Тесты написаны с использованием:
- **pytest** — фреймворк для управления тестами и фикстурами
- **allure-pytest** — генерация отчётов и логирования метаданных (эпик, фича, теги и т.д.)
- **Pydantic** — для валидации ответа от API
- **tools.assertions** — кастомные проверки (статус-код, структура ответа, JSON-схема)

Теги: `@pytest.mark.regression`, `@allure.tag(AllureTag.AUTHENTICATION)`
Сценарии: авторизация пользователя, защита от неавторизованных запросов

Требования:
    - Сервис аутентификации должен быть доступен
    - Фикстуры `function_user`, `authentication_client` должны возвращать валидные объекты
    - Библиотеки: `pytest`, `allure`, `httpx` (в клиенте), `Pydantic`, `jsonschema`

Пример запуска:
    pytest -m authentication -v testdata/tests/authentication/test_authentication.py
"""

from http import HTTPStatus
import allure
import pytest
from allure_commons.types import Severity
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_client_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.users import UserFixture
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    """
    Тестовый класс для проверки API аутентификации (вход пользователя).

    Метаданные Allure:
        - Эпик: LMS (Learning Management System)
        - Фича: Authentication
        - Теги: regression, authentication
        - Критичность: BLOCKER (блокирующий уровень)

    Все тесты:
        - используют фикстуру `function_user` — авторизованного пользователя
        - используют фикстуру `authentication_client` — клиент API
        - проверяют только успешные сценарии (CORRECT_CREDENTIALS)
    """
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Test with correct email and password")
    def test_login(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        """
        Сценарий: Успешный вход пользователя с корректными email и паролем.

        Выполняет:
        1. Формирует запрос `LoginRequestSchema` на основе данных `function_user`.
        2. Отправляет POST-запрос на эндпоинт аутентификации через `authentication_client.login_api()`.
        3. Валидирует:
           - Статус-код ответа (ожидается 200 OK)
           - Структуру ответа через Pydantic-схему `LoginResponseSchema`
           - JSON-схему ответа (генерируется из модели Pydantic)

        Аргументы:
            function_user (UserFixture): Фикстура с зарегистрированным пользователем.
            authentication_client (AuthenticationClient): Клиент для взаимодействия с API.

        Проверки:
            ✅ `assert_status_code(response.status_code, HTTPStatus.OK)`
            ✅ `assert_login_response(response_data)` — валидация бизнес-логики ответа
            ✅ `validate_json_schema(response.json(), response_data.model_json_schema())`

        Ожидаемый ответ:
            {
              "token": {
                "accessToken": "abc.def.ghi",
                "refreshToken": "xyz.123.456"
              },
              "user": {
                "id": "uuid",
                "email": "user@example.com",
                ...
              }
            }
        """
        request = LoginRequestSchema(email=function_user.email, password=function_user.password)
        response = authentication_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())






