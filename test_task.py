import httpx
from pydantic import BaseModel

from tools.assertions.schema import validate_json_schema


class EndpointsSchema(BaseModel):
    free : str
    pro : str
    health : str
    features: set

class TaskSchema(BaseModel):
    name: str
    version : float
    description : str
    documentation : str
    endpoints : EndpointsSchema






def test_get_list__of_users():
    request = 'https://reqres.in/api/'
    response = httpx.get(request)
    response_data = response.json()
    print(response.status_code)
    print(response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())
