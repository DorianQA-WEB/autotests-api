"""
Автоматизированный сценарий создания пользователя, загрузки файла и создания курса через API.

Этот скрипт демонстрирует полный цикл взаимодействия с микросервисами платформы:
1. Регистрация нового пользователя.
2. Аутентификация созданного пользователя.
3. Загрузка файла (например, изображения) на сервер.
4. Создание учебного курса с использованием загруженного файла как превью.

Используется для интеграционных тестов, сидирования данных или демонстрации API.

Пример использования:
    python api_client_create_course.py

Требует наличия файла './testdata/files/space.jpg'.
"""
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.file_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.user_schema import CreateUserRequestSchema

"""
Клиент для работы с публичными методами API пользователей.
Используется для регистрации нового пользователя без аутентификации.
"""
public_users_client = get_public_users_client()

"""
Запрос на создание пользователя. Генерирует уникальные email и пароль автоматически.
"""
# Создаем пользователя
create_user_request = CreateUserRequestSchema()

"""
Ответ от сервера с данными созданного пользователя (включая ID, email, статус).
"""
create_user_response = public_users_client.create_user(create_user_request)

# Инициализируем клиенты
"""
Объект аутентификации, содержащий учетные данные нового пользователя.
Используется для авторизации в других сервисах (files, courses и т.д.).
"""
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
"""
Клиент для работы с файловым сервисом. Авторизован под новым пользователем.
Позволяет загружать, скачивать и удалять файлы.
"""
files_client = get_files_client(authentication_user)

"""
Клиент для управления курсами. Авторизован под новым пользователем.
Позволяет создавать, редактировать и получать курсы.
"""
courses_client = get_courses_client(authentication_user)

# Загружаем файл
"""
Запрос на загрузку файла. Указывает путь к локальному файлу, который будет отправлен на сервер.
Поддерживаемые типы: изображения, документы (в зависимости от бэкенда).
"""
create_file_request = CreateFileRequestSchema(upload_file="./testdata/files/space.jpg")
"""
Ответ от сервера с информацией о загруженном файле:
- id — уникальный идентификатор файла
- имя, URL, метаданные
"""
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создаем курс
"""
Запрос на создание курса. Использует:
- ID загруженного файла как превью курса
- ID пользователя как создателя курса
Дополнительные поля (название, описание) могут быть добавлены по необходимости.
"""
create_course_request = CreateCourseRequestSchema(
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id
)

"""
Ответ от сервера с данными созданного курса:
- id — идентификатор курса
- previewFileId — ссылка на превью
- createdBy — ID автора
"""
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)