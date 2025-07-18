from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercise_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.users.user_schema import CreateUserRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.files.files_client import get_files_client
from clients.files.file_schema import CreateFileResponseSchema, CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client


public_users_client = get_public_users_client()

# Создаем пользователя
create_user_request = CreateUserRequestSchema(
)
# Используем метод create_user
create_user_response = public_users_client.create_user(create_user_request)


authentication_user = AuthenticationUserSchema(
    email= create_user_request.email,
    password= create_user_request.password
)
# Инициализируем клиенты
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercise_client = get_exercise_client(authentication_user)

# Загружаем файл
create_file_request = CreateFileRequestSchema(upload_file='./testdata/files/space.jpg')
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создаем курс
create_course_request = CreateCourseRequestSchema(
    previewFileId= create_file_response.file.id,
    createdByUserId= create_user_response.user.id
)
create_course_response = courses_client.create_course(create_course_request)
print('Create Course data:', create_course_response)

# создаем задание
create_exercise_request = CreateExerciseRequestSchema(
    id=create_user_response.user.id,
    course_id=create_course_response.course.id,
)
create_exercise_response = exercise_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)