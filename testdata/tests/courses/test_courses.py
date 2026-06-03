"""
Интеграционные тесты для API управления курсами (создание, получение, обновление).

Этот модуль содержит полный набор регрессионных тестов для проверки CRUD-операций над учебными курсами:
- `test_create_course`: создание нового курса с привязкой к файлу и пользователю;
- `test_get_courses`: получение списка курсов по ID пользователя;
- `test_update_course`: обновление данных существующего курса.

Тесты используют:
- pytest для организации и управления сценариями;
- allure для декорирования метаданными (эпик, фича, теги, критичность);
- Pydantic-модели для валидации запросов и ответов;
- кастомные ассерты (`assert_create_course_response` и др.) — для бизнес-проверок;
- `validate_json_schema` — для строгой проверки структуры ответа по JSON-схеме.

Теги: `@pytest.mark.courses`, `@pytest.mark.regression`
Эпик: `AllureEpic.LMS`
Фича: `AllureFeature.COURSES`

Зависимости:
    - fixtures.users, fixtures.files, fixtures.courses — для создания сущностей
    - clients.courses — клиент API курсов
    - tools.assertions.courses — кастомные проверки ответов
    - tools.allure — константы для метаданных Allure

Требования:
    - Сервис курсов должен быть доступен;
    - Должна быть возможность загрузки файлов и регистрации пользователей;
    - API должен возвращать корректные HTTP-статусы (200 OK).

Пример запуска:
    pytest -m courses -v testdata/tests/courses/test_courses.py --alluredir=allure-results
"""

from http import HTTPStatus
import pytest
import allure
from allure_commons.types import Severity
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, GetCoursesQuerySchema, GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_update_course_response, assert_get_courses_response, assert_create_course_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.COURSES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
class TestCourses:
    """
    Класс интеграционных тестов для API управления курсами.

    Метаданные Allure:
        - Эпик: LMS (Learning Management System)
        - Фича: Courses (управление курсами)
        - Критичность: BLOCKER для создания и получения, CRITICAL — для обновления
        - Теги: regression, courses

    Проверяет:
        ✅ Создание курса
        ✅ Получение списка курсов по пользователю
        ✅ Обновление курса

    """
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.title("Create course")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course(self,
                           function_files: FileFixture,
                           courses_client: CoursesClient,
                           function_user: UserFixture
                           ):
        """
        Сценарий: Успешное создание учебного курса с превью-изображением.

        Выполняет:
        1. Формирует запрос `CreateCourseRequestSchema`:
            - `created_by_user_id` — ID пользователя из `function_user`
            - `preview_file_id` — ID загруженного файла из `function_files`
        2. Отправляет POST-запрос на эндпоинт создания курса.
        3. Валидирует:
            - Статус-код (200 OK)
            - Структуру ответа через `CreateCourseResponseSchema`
            - JSON-схему ответа (генерируется из Pydantic-модели)
            - Бизнес-логику: `assert_create_course_response(request, response_data)`

        Аргументы:
            function_files (FileFixture): Загруженный файл как превью курса.
            courses_client (CoursesClient): Авторизованный клиент для создания курса.
            function_user (UserFixture): Пользователь — создатель курса.

        Ожидаемый ответ:
            {
              "course": {
                "id": "uuid",
                "title": null,
                "description": null,
                "previewFileId": "file-id",
                "createdByUserId": "user-id",
                "createdAt": "2024-01-01T00:00:00Z"
              }
            }
        """
        request = CreateCourseRequestSchema(
            created_by_user_id=function_user.response.user.id,
            preview_file_id=function_files.response.file.id)
        response = courses_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)


        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Get courses")
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    def test_get_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_course: CourseFixture,
            ):
        """
        Сценарий: Проверка получения списка курсов по ID пользователя.

        Выполняет:
        1. Формирует запрос к эндпоинту `GET /api/v1/courses` с параметром `user_id`.
        2. Проверяет, что в ответе присутствует курс, созданный в `function_course`.
        3. Валидирует:
            - Статус-код (200 OK)
            - Структуру `GetCoursesResponseSchema`
            - JSON-схему ответа
            - Бизнес-логику: `assert_get_courses_response([function_course.response])`

        Аргументы:
            courses_client (CoursesClient): Клиент API курсов.
            function_user (UserFixture): Пользователь, чьи курсы запрашиваются.
            function_course (CourseFixture): Курс, созданный в рамках фикстуры и ожидающийся в списке.

        Ожидаемый ответ:
            {
              "courses": [
                {
                  "id": "course-id",
                  "title": null,
                  ...
                }
              ]
            }
        """
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        response = courses_client.get_courses_api(query)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(response_data, [function_course.response])

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("Update course")
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        """
         Сценарий: Успешное обновление существующего курса.

         Выполняет:
         1. Формирует запрос `UpdateCourseRequestSchema` (с минимальными полями — как на усмотрение API).
         2. Отправляет PUT-запрос по ID курса из `function_course`.
         3. Валидирует:
             - Статус-код (200 OK)
             - Структуру ответа `UpdateCourseResponseSchema`
             - JSON-схему
             - Бизнес-логику: `assert_update_course_response(request, response_data)`

         Аргументы:
             courses_client (CoursesClient): Клиент API курсов.
             function_course (CourseFixture): Обновляемый курс.

         Ожидаемый ответ:
             {
               "course": {
                 "id": "uuid",
                 "title": "Новое название (если изменено)",
                 ...
               }
             }
         """
        request = UpdateCourseRequestSchema()
        response = courses_client.update_course_api(function_course.response.course.id, request)
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)


        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


