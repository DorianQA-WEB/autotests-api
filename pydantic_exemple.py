from pydantic import BaseModelб, Field




class Address(BaseModel):
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = Field(alias="isActive")
    address: Address

user = User(id=1,
            name='Alice',
            email="alice@exemple.com",
            address={'city':"Moscow", 'zip_code':'111111'})
print(user)
# user в формате словарь
print(user.model_dump())
# user в формате json
print(user.model_dump_json())