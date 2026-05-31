"""
Фикстуры pytest для работы с учебными заданиями в интеграционных и функциональных тестах.

Этот модуль предоставляет:
1. Клиент для взаимодействия с API заданий (авторизованный под тестовым пользователем).
2. Фикстуру, создающую тестовое задание, привязанное к курсу.

Зависимости:
    - clients.exercises — клиентская обёртка для API заданий
    - fixtures.users, fixtures.files, fixtures.courses — фикстуры для создания зависимых сущностей
    - pydantic — для типизации данных через BaseModel
    - pytest — для объявления и управления фикстурами

Используется в тестах, где требуется предварительно созданное задание (например, для проверки доступа, редактирования, получения или удаления).
"""
import pytest
from pydantic import BaseModel

from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.users import UserFixture
from fixtures.files import FileFixture
from fixtures.courses import CourseFixture
from clients.exercises.exercises_client import get_exercise_client, ExercisesClient



class ExerciseFixture(BaseModel):
    """
    Модель данных для фикстуры учебного задания.

    Атрибуты:
        request (CreateExerciseRequestSchema): Данные, использованные при создании задания.
        response (CreateExerciseResponseSchema): Ответ от API с данными созданного задания.
    """
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercise_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура: возвращает клиент для API заданий, авторизованный под тестовым пользователем.

    Зависит от `function_user`, который предоставляет объект аутентификации (email + пароль).

    Аргументы:
        function_user (UserFixture): Фикстура активного пользователя.

    Возвращает:
        ExercisesClient: Готовый к использованию клиент с JWT-токеном.

    Область видимости: function (по умолчанию). Новый клиент создаётся для каждого теста.
    """
    return get_exercise_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
        exercise_client: ExercisesClient,
        function_user: UserFixture,
        function_files: FileFixture,
        function_course: CourseFixture
) -> ExerciseFixture:
    """
    Фикстура: создаёт новое учебное задание и возвращает его данные.

    Полный цикл:
    1. Использует ID курса из `function_course.response.course.id` как родительский курс.
    2. Выполняет запрос `create_exercise` через авторизованный `exercise_client`.
    3. Возвращает объект `ExerciseFixture` с параметрами запроса и ответом.

    Аргументы:
        exercise_client (ExercisesClient): Авторизованный клиент для создания задания.
        function_user (UserFixture): Пользователь (не используется напрямую, но требуется как зависимость).
        function_files (FileFixture): Файл (не используется напрямую, может быть задействован в будущем).
        function_course (CourseFixture): Курс, к которому привязывается задание.

    Возвращает:
        ExerciseFixture: Объект, содержащий:
            - request: параметры создания задания (course_id)
            - response: ответ API с ID задания и метаданными

    Пример использования в тесте:

        def test_get_exercise(function_exercise: ExerciseFixture):
            exercise_id = function_exercise.response.exercise.id
            # ... выполнить GET запрос на получение задания

    ⚠️ Примечание:
        Задание создаётся при каждом вызове фикстуры. Убедитесь, что API или тестовая среда корректно очищает данные после теста,
        либо реализуйте финализатор (через yield), если требуется гарантированное удаление.
    """
    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course.id)
    response = exercise_client.create_exercise(request)

    return ExerciseFixture(request=request, response=response)