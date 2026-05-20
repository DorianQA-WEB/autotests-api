"""
Клиент для аутентификации и выполнения авторизованных запросов к API.

Этот скрипт демонстрирует:
1. Аутентификацию пользователя по email и паролю.
2. Получение JWT-токена (access token).
3. Создание постоянного HTTP-клиента с базовой авторизацией.
4. Выполнение защищённого запроса к эндпоинту `GET /api/get/users/me`.
Используется для:
    - Тестирования авторизованных эндпоинтов
    - Интеграционных проверок
    - Автоматизации API-взаимодействия

Зависимости:
    - httpx (установка: pip install httpx)

Пример запуска:
    python httpx_client.py
"""
import httpx

# Проходим аутентификацию
"""
Тело запроса для входа в систему.

Поля:
    - email: адрес электронной почты пользователя
    - password: пароль (в тестовых целях — "string")

⚠️ ВНИМАНИЕ: Указан неверный URL аутентификации. `https://reqres.in/api-docs/#/default/post_login`
не является рабочим эндпоинтом для получения JWT с полем `accessToken`. Этот сервис не поддерживает
аутентификацию в таком формате.

✅ Рекомендуемый URL:
    "http://localhost:8000/api/v1/authentication/login"
"""
login_payload = {
    "email": "user@example.com",
    "password": "string"
}

login_response = httpx.post("https://reqres.in/api-docs/#/default/post_login", json=login_payload)
login_response_data = login_response.json()
"""
Ответ от сервера аутентификации.

Ожидается структура:
{
  "token": {
    "accessToken": "abc.def.ghi",
    "refreshToken": "xyz.123.456"
  }
}
"""
print('Login data:', login_response_data)

# Инициализируем клиент с авторизацией
"""
Создание постоянного HTTP-клиента с:
    - Базовым URL: https://localhost:8000
    - Таймаутом: 100 секунд
    - Авторизационным заголовком: Bearer-токен из ответа логина

Все последующие запросы через этот клиент будут автоматически содержать заголовок Authorization.

⚠️ Опасность: Если `login_response_data` не содержит `token.accessToken`, возникнет KeyError.
Рекомендуется добавить проверку статуса и обработку исключений.
"""
client = httpx.Client(
    base_url="https://localhost:8000",
    timeout=100,
    headers={"Authorization": f"Bearer {login_response_data['token']['accessToken']}"}
)

# Выполняем запрос с авторизацией
"""
GET-запрос к защищённому эндпоинту, возвращающему данные текущего пользователя.

Ожидаемый ответ:
    - 200 OK + данные пользователя
    - 401 Unauthorized — если токен недействителен или отсутствует

Путь `api/get/users/me` может быть неточным. Вероятно, должен быть:
    - `/api/v1/users/me` или аналогичный.
"""
get_user_me_response = client.get("api/get/users/me")
get_user_me_response_data = get_user_me_response.json()
print('Get user me data:', get_user_me_response_data)