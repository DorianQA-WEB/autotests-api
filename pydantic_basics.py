"""
{
  "course": {
    "id": "string",
    "title": "string",
    "maxScore": 0,
    "minScore": 0,
    "description": "string",
    "previewFile": {
      "id": "string",
      "filename": "string",
      "directory": "string",
      "url": "https://example.com/"
    },
    "estimatedTime": "string",
    "createdByUser": {
      "id": "string",
      "email": "user@example.com",
      "lastName": "string",
      "firstName": "string",
      "middleName": "string"
    }
  }
}

"""
import uuid
from pydantic import BaseModel, Field, ConfigDict, computed_field, HttpUrl, EmailStr, ValidationError


# Модель FileSchema
class FileShema(BaseModel):
    id: str
    url: HttpUrl #Используем HttpUrl вместо str
    filename: str
    directory: str

# Модель UserSchema
class UserShema(BaseModel):
    id: str
    email: EmailStr # Используем EmailStr вместо str
    last_name: str = Field(alias="LastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    def get_username(self) -> str:
        return f"{self.first_name}{self.last_name}"


# Модель CourseSchema
class CourseSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Playwright"
    max_score: int = Field(alias="maxScore", default=1000)
    min_score: int = Field(alias="minScore", default=10)
    description: str = "Playwright course"
    # Вложенный объект для файла-превью
    preview_file: FileShema = Field(alias="previewFile")
    estimated_time: str = Field(alias="estimatedTime", default="2 weeks")
    # Вложенный объект для, пользователя создавшего курс
    created_by_user: UserShema = Field(alias="createdByUser")

# Инициализируем модель CourseSchema через передачу аргументов
course_default_model = CourseSchema(
    id="course-id",
    title="Playwright",
    maxScore=100,
    minScore=10,
    description="Playwright",
# Инициализация вложенной модели FileSchema
    previewFile=FileShema(
        id="file_id",
        url='http://localhost:8000',
        filename='file.png',
        directory="courses"
    ),
    estimatedTime="1 week",
# Инициализация вложенной модели UserSchema
    createdByUser=UserShema(
        id='user_id',
        email= "user@gmail.com",
        LastName="Bond",
        firstName="Zara",
        middleName="Alice"
    )
)


print('course_default_model:', course_default_model)


# Инициализируем модель CourseSchema через распаковку словаря
course_dict = {
    "id": "course-id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "description": "Playwright",
    # Ключ previewFile
    "previewFile": {
        "id": "file_id",
        "url": "http://localhost:8000",
        "filename": "file.png",
        "directory": "courses"
    },
    "estimatedTime": "1 week",
    # Ключ createdByUser
    "createdByUser":{
        'id': 'user_id',
        'email': "user@gmail.com",
        'LastName': "Bond",
        'firstName': "Zara",
        'middleName':  "Alice"
    }
}

course_dict_model = CourseSchema(**course_dict)
print("Course dict model:", course_dict_model)
print(course_dict_model.model_dump())
print(course_dict_model.model_dump_json(by_alias=True))


# Инициализируем модель CourseSchema через JSON
course_json = """
{
    "id": "course-id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "description": "Playwright",
    "previewFile": {
        "id": "file_id",
        "url": "http://localhost:8000",
        "filename": "file.png",
        "directory": "courses"
},
    "estimatedTime": "1 week",
    "createdByUser":{
        'id': 'user_id',
        'email': "user@gmail.com",
        'LastName': "Bond",
        'firstName': "Zara",
        'middleName':  "Alice"
    }
}
"""
course_json_model = CourseSchema.model_validate_json(course_json)
print("Course JSON model:", course_json_model)


# Инициализируем FileSchema c некорректным url
try:
    file = FileShema(
    id="file_id",
    url='htt//localho000',
    filename='file.png',
    directory="courses"
)
except ValidationError as error:
    print(error)
    print(error.errors())