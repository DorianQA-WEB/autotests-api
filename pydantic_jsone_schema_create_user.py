from clients.users.public_users_client import get_public_users_client
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
import jsonschema


public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
# Используем метод create_user
create_user_response = public_users_client.create_user_api(create_user_request)
create_user_response_schema = CreateUserResponseSchema.model_json_schema()

validate_json_schema(instance=create_user_response.json(), schema=create_user_response_schema)