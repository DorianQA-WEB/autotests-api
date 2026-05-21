"""
Тестовая реализация создания пользователя с валидацией JSON-схемы ответа.

Этот скрипт демонстрирует:
1. Генерацию данных для нового пользователя с использованием фейковых значений.
2. Отправку запроса на создание пользователя через API.
3. Получение JSON-схемы Pydantic-модели `CreateUserResponseSchema`.
4. Валидацию структуры ответа от API по этой схеме.

Используется для интеграционного тестирования: гарантирует, что API возвращает данные в ожидаемом формате.

Зависимости:
    - Pydantic (для моделей и генерации JSON-схем)
    - jsonschema (для валидации ответа)
    - Клиентская обёртка `public_users_client` для взаимодействия с API
Пример запуска:
    python pydantic_jsone_schema_create_user.py

Ожидаемый результат:
    - Успешное выполнение без исключений, если ответ соответствует схеме.
    - Ошибка валидации (jsonschema.ValidationError), если структура ответа нарушена.
"""
from clients.users.public_users_client import get_public_users_client
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
import jsonschema

"""
Клиент для работы с эндпоинтом регистрации пользователей.
Не требует аутентификации. Используется для отправки запроса `create_user_api`.
"""
public_users_client = get_public_users_client()

"""
Объект запроса на создание пользователя.

Поля:
    - email: уникальный адрес, генерируется через `fake.email()`
    - password: тестовый пароль (фиксированный)
    - last_name, first_name, middle_name: фиктивные строковые значения

Pydantic автоматически валидирует данные при создании экземпляра.
"""
create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)

# Используем метод create_user
"""
POST-запрос к API: `/api/v1/users` или аналогичный.

Ожидается:
    - Статус 201 Created
    - Тело ответа в формате JSON с данными созданного пользователя

Ответ должен соответствовать структуре `CreateUserResponseSchema`.
"""
create_user_response = public_users_client.create_user_api(create_user_request)

# Получаем JSON схему из модели ответа
"""
Генерация JSON-схемы на основе Pydantic-модели `CreateUserResponseSchema`.

Схема описывает:
    - Структуру поля `user`
    - Ожидаемые типы полей (id — UUID, email — string, и т.д.)
    - Обязательные и опциональные поля

Используется как эталон для валидации реального ответа от API.
"""

create_user_response_schema = CreateUserResponseSchema.model_json_schema()

# Проверяем, что JSON-ответ от API соответствует ожидаемой JSON-схеме
"""
Проверка, что тело ответа от API соответствует ожидаемой JSON-схеме.

Если структура ответа отличается (например, отсутствует поле `id`, неверный тип `email`),
будет выброшено исключение `jsonschema.exceptions.ValidationError`.

✅ Это обеспечивает:
    - Соответствие API контракту
    - Раннее выявление брейкинг-изменений
    - Надёжность интеграций
"""

validate_json_schema(instance=create_user_response.json(), schema=create_user_response_schema)