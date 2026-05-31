"""
Фикстуры pytest для работы с курсами в интеграционных и функциональных тестах.

Этот модуль предоставляет фикстуры, которые:
1. Создают клиент для взаимодействия с API курсов.
2. Автоматически создают тестовый курс с привязкой к пользователю и файлу.

Зависимости:
    - clients.courses — клиентская обёртка для API курсов
    - fixtures.users, fixtures.files — зависимости для создания пользователя и загрузки файла
    - pydantic — для типизации фикстур через BaseModel
    - pytest — для объявления и управления фикстурами

Используется в тестах, где требуется предварительно созданный курс (например, для создания заданий, проверки доступа, редактирования).
"""
import pytest
from pydantic import BaseModel

from clients.courses.courses_client import CoursesClient, get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.files import FileFixture
from fixtures.users import UserFixture


class CourseFixture(BaseModel):
    """
    Модель данных для фикстуры курса.

    Атрибуты:
        request (CreateCourseRequestSchema): Данные, отправленные при создании курса.
        response (CreateCourseResponseSchema): Ответ от API с данными созданного курса.
    """
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema


@pytest.fixture
def courses_client(function_user: UserFixture) -> CoursesClient:
    """
    Фикстура: возвращает клиент для API курсов, авторизованный под тестовым пользователем.

    Зависит от `function_user`, который предоставляет объект аутентификации (email + пароль).

    Аргументы:
        function_user (UserFixture): Фикстура активного пользователя.

    Возвращает:
        CoursesClient: Готовый к использованию клиент с JWT-токеном.

    Область видимости: function (по умолчанию). Новый клиент создаётся для каждого теста.
    """
    return get_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(
        courses_client: CoursesClient,
        function_user: UserFixture,
        function_files: FileFixture
) -> CourseFixture:
    """
    Фикстура: создаёт новый учебный курс с превью и возвращает его данные.

    Полный цикл:
    1. Использует ID загруженного файла (`function_files.response.file.id`) как превью.
    2. Устанавливает создателем пользователя из `function_user`.
    3. Выполняет запрос `create_course` через `courses_client`.
    4. Возвращает объект `CourseFixture` с запросом и ответом.

    Аргументы:
        courses_client (CoursesClient): Авторизованный клиент для создания курса.
        function_user (UserFixture): Пользователь, который будет указан как создатель.
        function_files (FileFixture): Загруженный файл, используемый как превью курса.

    Возвращает:
        CourseFixture: Объект, содержащий:
            - request: параметры создания курса
            - response: ответ API с ID курса и метаданными

    Пример использования в тесте:

        def test_get_course(function_course: CourseFixture):
            course_id = function_course.response.course.id
            # ... выполнить GET запрос на получение курса

    ⚠️ Примечание:
        Курс создаётся при каждом вызове фикстуры. Убедитесь, что API поддерживает очистку данных после теста,
        либо реализуйте финализатор (например, через yield или finalizer).
    """
    request = CreateCourseRequestSchema(
        preview_file_id=function_files.response.file.id,
        created_by_user_id=function_user.response.user.id
)
    response = courses_client.create_course(request)
    return CourseFixture(request=request, response=response)