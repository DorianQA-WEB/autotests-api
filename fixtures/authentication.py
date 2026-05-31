"""
Фикстура для предоставления клиента аутентификации в тестах.

Этот модуль содержит pytest-фикстуру, которая инициализирует и возвращает клиент для работы
с API аутентификации. Используется в интеграционных и функциональных тестах, где требуется
выполнить вход пользователя, обновление токенов или проверка авторизационных сценариев.

Функционал:
    - Предоставляет изолированный экземпляр `AuthenticationClient`
    - Гарантирует повторяемость тестов за счёт централизованного создания клиента
    - Поддерживает dependency injection в тестовые функции через механизм фикстур pytest

Зависимости:
    - clients.authentication.authentication_client — клиентская обёртка для API аутентификации
    - pytest — фреймворк для управления фикстурами

Пример использования в тесте:

    def test_user_login(authentication_client: AuthenticationClient):
        response = authentication_client.login(email="user@example.com", password="string")
        assert response.status_code == 200

"""
from clients.authentication.authentication_client import get_authentication_client, AuthenticationClient
import pytest



@pytest.fixture
def authentication_client() -> AuthenticationClient:
    """
    Фикстура: создаёт и возвращает клиент для взаимодействия с API аутентификации.

    Использует фабричную функцию `get_authentication_client()` для получения
    настроенного экземпляра `AuthenticationClient`.

    Возвращаемое значение:
        AuthenticationClient: Авторизованный или неавторизованный HTTP-клиент,
                              готовый к вызову методов:
                              - login()
                              - refresh_token()
                              - logout() (если реализовано)

    Область видимости:
        По умолчанию — функция (function-scope). Клиент создаётся заново для каждого теста.
        При необходимости можно изменить на `scope="module"` или `session`.

    Примечания:
        - Фикстура типизирована для поддержки IDE и mypy.
        - Рекомендуется использовать данную фикстуру вместо прямого вызова `get_authentication_client()`
          в тестах для соблюдения принципов чистоты и переиспользования.
    """
    return get_authentication_client()


