from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    ExercisesSchema, GetExercisesQuerySchema
from tools.assertions.base import assert_equal, assert_length


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
    Проверяет, что фактические данные курса соответствуют ожидаемым.

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
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
        get_exercise_response: GetExercisesQuerySchema,
        create_exercise_response: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.

    :param get_exercise_response: Ответ API при запросе списка курсов.
    :param create_exercise_response: Список API ответов при создании курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_length(get_exercise_response.exercise, create_exercise_response, "exercise")


    for index, create_exercise_response in enumerate(create_exercise_response):
        assert_exercise(get_exercise_response.exrcise[index], create_exercise_response.course)

