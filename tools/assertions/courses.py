from clients.courses.courses_schema import UpdateCourseResponseSchema, UpdateCourseRequestSchema, CourseSchema, \
    GetCoursesResponseSchema, CreateCourseRequestSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user


def assert_update_course_response(
        request: UpdateCourseRequestSchema,
        response: UpdateCourseResponseSchema
):
    """
    Проверяет, что фактические данные на обновление курса соответствуют ожидаемым.

    :param request: Фактические данные курса.
    :param response: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


def assert_course(
        actual: CourseSchema,
        expected: CourseSchema
):
    """
    Проверяет, что фактические данные курса соответствуют ожидаемым.

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    assert_file(actual.previewFile, expected.previewFile)
    assert_user(actual.createdByUser, expected.createdByUser)


def assert_get_courses_response(
        get_courses_response: GetCoursesResponseSchema,
        create_course_responses: list[GetCoursesResponseSchema]
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.

    :param get_courses_response: Ответ API при запросе списка курсов.
    :param create_course_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_length(get_courses_response.courses, create_course_responses, "courses")


    for index, create_course_response in enumerate(create_course_responses):
        assert_course(get_courses_response.courses[index], create_course_response.course)


def assert_create_course_response(
        request: CreateCourseRequestSchema,
        response: CreateCourseRequestSchema
):
    """
    Проверяет, что фактические данные курса соответствуют ожидаемым.

    :param request: Фактические данные курса.
    :param response: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(request.title, response.title, "title")
    assert_equal(request.max_score, response.max_score, "max_score")
    assert_equal(request.min_score, response.min_score, "min_score")
    assert_equal(request.description, response.description, "description")
    assert_equal(request.estimated_time, response.estimated_time, "estimated_time")
    assert_equal(request.preview_file_id, response.preview_file_id, "preview_file_id")
    assert_equal(request.created_by_user_id, response.created_by_user_id, "created_by_user_id")