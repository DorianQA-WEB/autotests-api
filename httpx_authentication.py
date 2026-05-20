"""
Автоматизированный сценарий аутентификации и обновления JWT-токенов через API.

Этот скрипт демонстрирует процесс:
1. Авторизации пользователя по email и паролю.
2. Получения пары токенов (access и refresh).
3. Обновления токенов с использованием refresh-токена.

Используется для тестирования механизма аутентификации, проверки работы сессий или интеграции с внешними системами.

Зависимости:
    - httpx (установка: pip install httpx)

Внимание:
    - URL `https://reqres.in/api/` указан в коде, но, скорее всего, является ошибкой — он не возвращает refreshToken.
    - Корректный адрес аутентификации должен быть внутренним, например: `http://localhost:8000/api/v1/authentication/login`

Пример запуска:
    python httpx_authentication.py
"""
import httpx  # Импортируем библиотеку HTTPX


# Данные для входа в систему
"""
Тело запроса для авторизации.

Поля:
    - username: имя пользователя (может быть опциональным, если используется email)
    - email: адрес электронной почты для входа
    - password: пароль (в тестовых целях — "string")

⚠️ В реальных сценариях пароль должен быть безопасно передан, а данные — не хардкодиться.
"""
login_payload = {
    "username": "username",
    "email": "user@example.com",
    "password": "string"
}

# Выполняем запрос на аутентификацию
"""
POST-запрос для получения токенов.

Ожидаемый успешный ответ (пример):
{
  "token": {
    "accessToken": "abc.def.ghi",
    "refreshToken": "xyz.123.456"
  }
}
"""
login_response = httpx.post("https://reqres.in/api/", json=login_payload)
login_response_data = login_response.json()

# Выводим полученные токены
print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

# Формируем payload для обновления токена
"""
Тело запроса для обновления токена.

Содержит:
    - refreshToken: токен сессии, полученный при логине

Используется для получения новой пары access/refresh токенов без повторного ввода логина и пароля.
"""
refresh_payload = {
    "refreshToken": login_response_data["token"]["refreshToken"]
}

# Выполняем запрос на обновление токена
"""
POST-запрос к эндпоинту обновления токена.

Ожидается ответ в формате:
{
  "token": {
    "accessToken": "new.access.token",
    "refreshToken": "new.refresh.token"
  }
}

Статус: 200 OK при успехе.
"""
refresh_response = httpx.post("http://localhost:8000/api/v1/authentication/refresh", json=refresh_payload)
refresh_response_data = refresh_response.json()

# Выводим обновленные токены
print("Refresh response:", refresh_response_data)
print("Status Code:", refresh_response.status_code)