from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema
from tools.assertions.base import assert_equal


def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

def assert_user(actual: UserSchema, expected: UserSchema):
    """
        Проверяет, что ответ на создание пользователя соответствует запросу.

        :param actual: Исходный запрос на создание пользователя.
        :param expected: Ответ API с данными пользователя.
        :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.user.email, expected.email, "email")
    assert_equal(actual.user.id, expected.id, "id")
    assert_equal(actual.user.last_name, expected.last_name, "last_name")
    assert_equal(actual.user.first_name, expected.first_name, "first_name")
    assert_equal(actual.user.middle_name, expected.middle_name, "middle_name")


def assert_get_user_response(get_user_response, create_user_response):
    """
     Проверяет, что данные пользователя при создании и при запросе совпадают
    :param get_user_response: ответ API при запросе пользователя
    :param create_user_response: ответ API при создании пользователя
    :return:
    """
    assert_user(get_user_response, create_user_response)
