from pydantic import BaseModel, Field, ConfigDict

class ExercisesSchema(BaseModel):
    """
    Описание структуры задания
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str =Field(alias="courseId")
    max_score: int =Field(alias="maxScore")
    min_score: int =Field(alias="minScore")
    order_index: int =Field(alias='orderIndex')
    description: str
    estimated_time: str =Field(alias="estimatedTime")

class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий.
    """
    course_id: str =Field(alias="courseId")


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    """
    model_config = ConfigDict(populate_by_name=True)


    id: str
    title: str
    course_id: str =Field(alias="courseId")
    max_score: int =Field(alias="maxScore")
    min_score: int =Field(alias="minScore")
    order_index: int =Field(alias='orderIndex')
    description: str
    estimated_time: str =Field(alias="estimatedTime")


class CreateExerciseResponseSchema(BaseModel):
    """
    Описание ответа на запрос создания задания.
    """
    exercise: ExercisesSchema


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания.
    """
    model_config = ConfigDict(populate_by_name=True)


    title: str | None
    max_score: int | None =Field(alias="maxScore")
    min_score: int | None =Field(alias="minScore")
    order_index: int | None =Field(alias='orderIndex')
    description: str | None
    estimated_time: str | None =Field(alias="estimatedTime")