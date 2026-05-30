# Autotests API

Проект автоматизированного тестирования REST API на базе **Python**, **pytest** и **httpx**.  
Предназначен для функционального тестирования, проверки контрактов (JSON Schema), генерации отчётов **Allure** и отслеживания покрытия API через **Swagger Coverage Tool**.

---

## Содержание

- [Стек технологий](#стек-технологий)
- [Структура проекта](#структура-проекта)
- [Установка и настройка](#установка-и-настройка)
- [Конфигурация](#конфигурация)
- [Запуск тестов](#запуск-тестов)
- [Генерация отчётов](#генерация-отчётов)
- [Отслеживание покрытия API](#отслеживание-покрытия-api)
- [Основные компоненты](#основные-компоненты)
- [Примеры использования](#примеры-использования)

---

## Стек технологий

| Компонент          | Технология                                                                 |
|--------------------|----------------------------------------------------------------------------|
| Язык               | Python 3.12+                                                               |
| Тестовый фреймворк | [pytest](https://docs.pytest.org/) 8.4                                     |
| HTTP-клиент        | [httpx](https://www.python-httpx.org/) 0.28                                |
| Валидация данных   | [Pydantic](https://docs.pydantic.dev/) 2.11                                |
| Генерация данных   | [Faker](https://faker.readthedocs.io/)                                     |
| Отчёты             | [Allure](https://docs.qameta.io/allure-report/) + `allure-pytest`          |
| Покрытие API       | [Swagger Coverage Tool](https://pypi.org/project/swagger-coverage-tool/)   |
| Конфигурация       | `pydantic-settings` + `.env`                                               |
| Параллельный запуск| `pytest-xdist`                                                             |
| Перезапуск тестов  | `pytest-rerunfailures`                                                     |

---

## Структура проекта

```
autotests-api/
├── clients/                          # HTTP-клиенты и схемы
│   ├── api_client.py                 # Базовый API-клиент (GET, POST, PATCH, DELETE)
│   ├── api_coverage.py               # Инициализация трекера покрытия Swagger
│   ├── errors_schema.py              # Pydantic-схемы ошибок API
│   ├── event_hooks.py                # Event hooks: cURL, логирование запросов/ответов
│   ├── private_http_builder.py       # Сборка клиента с аутентификацией (Bearer JWT)
│   ├── public_http_builder.py        # Сборка публичного клиента (без авторизации)
│   ├── authentication/               # Клиент и схемы аутентификации
│   ├── courses/                      # Клиент и схемы курсов
│   ├── exercises/                    # Клиент и схемы упражнений
│   ├── files/                        # Клиент и схемы файлов
│   └── users/                        # Клиенты и схемы пользователей (public/private)
├── fixtures/                         # Pytest-фикстуры
│   ├── users.py                      # Фикстуры пользователей
│   ├── files.py                      # Фикстуры файлов
│   ├── courses.py                    # Фикстуры курсов
│   ├── exercises.py                  # Фикстуры упражнений
│   ├── authentication.py             # Фикстуры аутентификации
│   └── allure.py                     # Фикстуры для Allure (environment.properties)
├── testdata/                         # Тестовые данные
│   ├── files/space.jpg               # Тестовое изображение для загрузки
│   └── tests/                        # Директория с тестами
│       ├── authentication/           # Тесты аутентификации
│       ├── courses/                  # Тесты курсов
│       ├── exercises/                # Тесты упражнений
│       ├── files/                    # Тесты файлов
│       ├── users/                    # Тесты пользователей
│       └── pytest/                   # Обучающие тесты по pytest
├── tools/                            # Вспомогательные утилиты
│   ├── assertions/                   # Кастомные ассерты (base, users, courses, files и т.д.)
│   ├── http/curl.py                  # Генерация cURL-команды из httpx.Request
│   ├── allure/                       # Allure-декораторы (epics, features, stories, tags)
│   ├── fakers.py                     # Генерация тестовых данных через Faker
│   ├── logger.py                     # Настройка логирования
│   └── routes.py                     # Enum с маршрутами API
├── config.py                         # Конфигурация приложения (pydantic-settings)
├── conftest.py                       # Глобальные фикстуры pytest
├── pytest.ini                        # Настройки pytest
├── requirements.txt                  # Зависимости проекта
└── .env                              # Переменные окружения (не в git)
```

---

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/DorianQA-WEB/autotests-api.git
cd autotests-api
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка окружения

Скопируйте файл `.env.example` в `.env` (если он есть) или создайте `.env` со следующим содержимым:

```ini
TEST_DATA.IMAGE_PNG_FILE="./testdata/files/space.jpg"
HTTP_CLIENT.URL="http://localhost:8000"
HTTP_CLIENT.TIMEOUT=100
SWAGGER_COVERAGE_SERVICES='[
    {
        "key": "api-course",
        "name": "API Course",
        "tags": ["API", "COURSES"],
        "repository": "https://github.com/DorianQA-WEB/autotests-api",
        "swagger_url": "http://localhost:8000/openapi.json"
    }
]'
SWAGGER_COVERAGE_HTML_REPORT_FILE="./coverage.html"
```

---

## Конфигурация

Конфигурация управляется через класс [`Settings`](config.py:42) на базе `pydantic-settings`.  
Значения загружаются из переменных окружения и файла `.env`.

| Параметр                  | Описание                                      | Значение по умолчанию |
|---------------------------|-----------------------------------------------|-----------------------|
| `HTTP_CLIENT.URL`         | Базовый URL тестируемого API                  | `http://localhost:8000` |
| `HTTP_CLIENT.TIMEOUT`     | Таймаут HTTP-запроса (сек.)                   | `100`                 |
| `TEST_DATA.IMAGE_PNG_FILE`| Путь к тестовому изображению                  | `./testdata/files/space.jpg` |
| `ALLURE_RESULTS_DIR`      | Директория для результатов Allure             | `./allure-results`    |
| `SWAGGER_COVERAGE_SERVICES`| JSON-список сервисов для отслеживания покрытия | —                     |

---

## Запуск тестов

### Все тесты

```bash
pytest
```

### Тесты по маркерам

```bash
pytest -m users          # Только тесты пользователей
pytest -m courses        # Только тесты курсов
pytest -m files          # Только тесты файлов
pytest -m exercises      # Только тесты упражнений
pytest -m authentication # Только тесты аутентификации
pytest -m regression     # Только регрессионные тесты
```

### Параллельный запуск

```bash
pytest -n auto
```

### Перезапуск упавших тестов

```bash
pytest --reruns 2
```

### С генерацией Allure-отчёта

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Генерация отчётов

### Allure Report

1. Запустите тесты с флагом `--alluredir`:

   ```bash
   pytest --alluredir=allure-results
   ```

2. Сформируйте и откройте отчёт:

   ```bash
   allure serve allure-results
   ```

Allure-декораторы распределены по файлам в [`tools/allure/`](tools/allure/):

- [`epics.py`](tools/allure/epics.py) — `@allure.epic`
- [`features.py`](tools/allure/features.py) — `@allure.feature`
- [`stories.py`](tools/allure/stories.py) — `@allure.story`
- [`tags.py`](tools/allure/tags.py) — `@allure.tag`

---

## Отслеживание покрытия API

Проект использует [Swagger Coverage Tool](https://pypi.org/project/swagger-coverage-tool/) для автоматического отслеживания того, какие эндпоинты API были покрыты тестами.

### Настройка

Конфигурация сервисов задаётся в переменной `SWAGGER_COVERAGE_SERVICES` в файле `.env`.  
Трекер инициализируется в [`clients/api_coverage.py`](clients/api_coverage.py:4):

```python
tracker = SwaggerCoverageTracker(service="api-course")
```

### Генерация отчёта

После прогона тестов выполните:

```bash
pytest
```

HTML-отчёт о покрытии будет сохранён в файл, указанный в `SWAGGER_COVERAGE_HTML_REPORT_FILE` (по умолчанию `coverage.html`).

---

## Основные компоненты

### API-клиенты

- [`APIClient`](clients/api_client.py:8) — базовый класс-обёртка над `httpx.Client` с поддержкой Allure-шагов.
- [`get_public_http_client()`](clients/public_http_builder.py:7) — создаёт клиент без авторизации.
- [`get_private_http_client(user)`](clients/private_http_builder.py:17) — создаёт клиент с JWT-токеном после логина.

### Event hooks

В [`clients/event_hooks.py`](clients/event_hooks.py) реализованы три hook-функции:

- [`curl_event_hook`](clients/event_hooks.py:12) — автоматически прикрепляет cURL-команду к Allure-отчёту.
- [`log_request_event_hook`](clients/event_hooks.py:23) — логирует исходящий запрос.
- [`log_response_event_hook`](clients/event_hooks.py:32) — логирует входящий ответ.

### Ассерты

Кастомные проверки расположены в [`tools/assertions/`](tools/assertions/):

- [`base.py`](tools/assertions/base.py) — базовые ассерты (статус-код, заголовки).
- [`schema.py`](tools/assertions/schema.py) — валидация JSON Schema через Pydantic.
- [`errors.py`](tools/assertions/errors.py) — проверки структуры ошибок.
- [`users.py`](tools/assertions/users.py), [`courses.py`](tools/assertions/courses.py), [`exercises.py`](tools/assertions/exercises.py), [`files.py`](tools/assertions/files.py) — доменные ассерты.

### Генерация тестовых данных

[`tools/fakers.py`](tools/fakers.py) — утилиты на базе библиотеки Faker для генерации email, паролей, имён и других данных.

### Маршруты API

[`tools/routes.py`](tools/routes.py) — Enum `APIRoutes` с путями всех эндпоинтов:

| Ресурс         | Путь                     |
|----------------|--------------------------|
| Пользователи   | `/api/v1/users`          |
| Файлы          | `/api/v1/files`          |
| Курсы          | `/api/v1/courses`        |
| Упражнения     | `/api/v1/exercises`      |
| Аутентификация | `/api/v1/authentication` |

---

## Примеры использования

### Простой тест пользователя

```python
import pytest
from clients.public_http_builder import get_public_http_client
from clients.api_client import APIClient
from tools.routes import APIRoutes


def test_get_users():
    client = APIClient(get_public_http_client())
    response = client.get(APIRoutes.USERS)
    assert response.status_code == 200
```

### Тест с аутентификацией

```python
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.api_client import APIClient
from tools.routes import APIRoutes


def test_get_user_profile():
    user = AuthenticationUserSchema(email="test@example.com", password="secret")
    client = APIClient(get_private_http_client(user))
    response = client.get(f"{APIRoutes.USERS}/me")
    assert response.status_code == 200
```

---

## Лицензия

Проект распространяется без явной лицензии. Используется в учебных и демонстрационных целях.