from clients.authentication.authentication_client_schema import LoginRequestSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
import jsonschema


public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
# Используем метод create_user
create_user_response = public_users_client.create_user(create_user_request)

# Запрос на получение данных о созданном пользователе с использованием метода API клиента
authentication_user = LoginRequestSchema(
    email=create_user_request.email,
    password=create_user_request.password)

private_users_client = get_private_users_client(authentication_user)

# Используем метод get_user
get_user_response = private_users_client.get_user_api(create_user_response.user.id)
get_user_response_schema = CreateUserResponseSchema.model_json_schema()
print(get_user_response_schema)

# Проверяем, что JSON-ответ от API соответствует ожидаемой JSON-схеме
validate_json_schema(instance=get_user_response.json(), schema=get_user_response_schema)