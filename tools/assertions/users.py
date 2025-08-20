from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema, \
    GetUserResponseSchema
from tools.assertions.base import assert_equal
import allure
from tools.logger import get_logger

logger = get_logger("USERS_ASSERTIONS")

@allure.step("Assert create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Assert create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Assert user")
def assert_user(actual: UserSchema, expected: UserSchema):
    """
        Проверяет, что ответ на создание пользователя соответствует запросу.

        :param actual: Исходный запрос на создание пользователя.
        :param expected: Ответ API с данными пользователя.
        :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Assert user")

    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


@allure.step("Assert get user response")
def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: CreateUserResponseSchema):
    """
     Проверяет, что данные пользователя при создании и при запросе совпадают
    :param get_user_response: ответ API при запросе пользователя
    :param create_user_response: ответ API при создании пользователя
    :raises AssertionError: Если данные пользователя не совпадают.
    """
    logger.info("Assert get user response")

    assert_user(get_user_response.user, create_user_response.user)
