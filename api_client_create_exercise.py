import clients
from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import CreateExerciseRequestDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from tools.fakers import get_random_email

public_users_client = get_public_users_client()

# Создаем пользователя
create_user_request = CreateUserRequestDict(
    email=get_random_email(),
    password="string",
    lastName="string",
    firstName="string",
    middleName="string"
)
# Используем метод create_user
create_user_response = public_users_client.create_user(create_user_request)


authentication_user = AuthenticationUserDict(
    email= create_user_request["email"],
    password= create_user_request['password']
)
# Инициализируем клиенты
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercise_client = get_courses_client(authentication_user)

# Загружаем файл
create_file_request = CreateFileRequestDict(
    filename='space.jpg',
    directory='courses',
    upload_file='./testdata/files/space.jpg'
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создаем курс
create_course_request = CreateCourseRequestDict(
    title="Python",
    maxScore=100,
    minScore= 10,
    description= "Python API course",
    estimatedTime= "2 weeks",
    previewFileId= create_file_response['file']['id'],
    createdByUserId= create_user_response['user']['id']
)
create_course_response = courses_client.create_course(create_course_request)
print('Create Course data:', create_course_response)

# создаем задание
create_exercise_request = CreateExerciseRequestDict(
    id=create_user_response['user']['id'],
    title="Python",
    maxScore=100,
    minScore= 10,
    courseId=create_course_response['course']['id'],
    orderIndex= 20,
    description= "Python API exercise",
    estimatedTime= "2 weeks",
)
create_exercise_response = exercise_client.create_course(create_exercise_request)
print('Create Exercise data:', create_exercise_response)