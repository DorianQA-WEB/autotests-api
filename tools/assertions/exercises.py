from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    ExercisesSchema, GetExercisesResponseSchema, UpdateExerciseRequestSchema, \
    UpdateExerciseResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response


def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание задания соответствуют запросу.

    :param request: Исходный запрос на создание задания.
    :param response: Ответ API с данными задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")
    assert_equal(response.exercise.description ,request.description, "description")


def assert_exercise(
        actual: ExercisesSchema,
        expected: ExercisesSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания.
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.order_index, expected.order_index, 'order_index')
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")
    assert_equal(actual.description, expected.description, "description")


def assert_get_exercise_response(
        get_exercise_response: GetExercisesResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.

    :param get_exercise_response: Ответ API при запросе данных задания.
    :param create_exercise_response: Ответ API при создании задания.
    :raises AssertionError: Если данные задания не совпадают.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """
    Проверяет, что фактические данные на обновление задания соответствуют ожидаемым.

    :param request: Фактические данные задания.
    :param response: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(request.title, response.title, "title")
    assert_equal(request.course_id, response.course_id, "course_id")
    assert_equal(request.min_score, response.min_score, "min_score")
    assert_equal(request.max_score, response.max_score, "max_score")
    assert_equal(request.order_index, response.order_index, 'order_index')
    assert_equal(request.estimated_time, response.estimated_time, "estimated_time")
    assert_equal(request.description, response.description, "description")


def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если задание не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Exercise not found"
    """
    expected = InternalErrorResponseSchema(detail="Exercise not found")
    assert_internal_error_response(actual, expected)


def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercises_responses: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка заданий соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка задания.
    :param create_exercises_responses: Список API ответов при создании задания.
    :raises AssertionError: Если данные задания не совпадают.
    """
    assert_length(get_exercises_response.exercises, create_exercises_responses, "exercises")

    for index, create_exercises_responses in enumerate(create_exercises_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercises_responses.exercise)
