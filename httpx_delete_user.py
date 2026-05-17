"""
Автоматизированный сценарий создания, аутентификации и удаления пользователя через HTTP-запросы.

Этот скрипт демонстрирует работу с REST API сервиса пользователей с использованием библиотеки `httpx`.
Полный цикл включает:
1. Создание нового пользователя.
2. Аутентификацию по email и паролю.
3. Удаление пользователя с использованием JWT-токена.

Используется для тестирования безопасности, валидации API или демонстрации CRUD-операций.

Зависимости:
    httpx
    faker (для генерации тестовых данных)

Пример запуска:
    python httpx_delete_user.py

Требования:
    - Сервис должен быть доступен на http://localhost:8000
    - Должна быть включена поддержка регистрации и авторизации
"""
import httpx

from tools.fakers import fake
"""
Модуль для генерации фейковых данных (email, имена и т.д.).
Используется для создания уникального пользователя при каждом запуске.
"""


# Создаем пользователя
"""
Тело запроса для создания пользователя.
Генерируется уникальный email через `fake.email()`, остальные поля — фиктивные.
Пароль указан как "string" — при необходимости можно заменить на более сложный.
"""
create_user_payload = {
    "email": fake.email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

"""
Отправка POST-запроса на создание пользователя.
Ожидается ответ 201 Created с данными нового пользователя (включая ID).
"""
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print('Create user data:', create_user_response_data)

# Проходим аутентификацию
"""
Данные для входа: email и пароль из ранее созданного пользователя.
"""
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}

"""
POST-запрос для получения JWT-токена.
Ожидается ответ с accessToken, который используется для авторизации в последующих запросах.
"""
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)

# Удаляем ранее созданного пользователя
"""
Заголовки для DELETE-запроса. Содержат Bearer-токен для авторизации.
Без токена запрос будет отклонён с ошибкой 401 Unauthorized.
"""
delete_user_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}

"""
DELETE-запрос на удаление пользователя по его ID.
Адрес формируется динамически на основе ID из ответа создания.
"""
delete_user_response = httpx.delete(
    f"http://localhost:8000/api/v1/users/{create_user_response_data['user']['id']}",
    headers=delete_user_headers
)

"""
Ожидается успешный ответ (например, 200 OK или 204 No Content) с подтверждением удаления.
"""
delete_user_response_data = delete_user_response.json()
print('Delete user data:', delete_user_response_data)