from pydantic import BaseModel, Field, ConfigDict
from clients.files.file_schema import FileSchema
from clients.users.user_schema import UserSchema


# описание структуры курса
class CourseSchema(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)


    id: str
    title: str
    max_score: int =Field(alias="maxScore")
    min_score: int =Field(alias="minScore")
    description: str
    previewFile: FileSchema  # Вложенная структура файла
    estimated_time: str =Field(alias="estimatedTime")
    createdByUser: UserSchema # Вложенная структура пользователя


class GetCoursesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов.
    """
    userId: str


class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание курса.
    """
    model_config = ConfigDict(populate_by_name=True)


    title: str
    max_score: int =Field(alias="maxScore")
    min_score: int =Field(alias="minScore")
    description: str
    estimated_time: str =Field(alias="estimatedTime")
    previewFileId: str
    createdByUserId: str


# описание структуры запроса на создание курса
class CreateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """
    course: CourseSchema


class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)


    title: str | None
    max_score: int | None =Field(alias="maxScore")
    min_score: int | None =Field(alias="minScore")
    description: str | None
    estimated_time: str | None =Field(alias="estimatedTime")