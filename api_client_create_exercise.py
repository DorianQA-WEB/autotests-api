"""
Автоматизированный сценарий создания пользователя, курса и учебного задания через API.

Этот скрипт демонстрирует полный цикл взаимодействия с микросервисами образовательной платформы:
1. Регистрация нового пользователя.
2. Аутентификация пользователя по email и паролю.
3. Загрузка файла (например, изображения) для использования в курсе.
4. Создание учебного курса с превью.
5. Создание учебного задания в рамках этого курса.

Используется для интеграционных тестов, сидирования тестовых данных или демонстрации API-возможностей.

Зависимости:
    - Клиентские SDK: users, files, courses, exercises
    - Pydantic для валидации данных
    - HTTP-клиент (например, httpx), инкапсулированный в private_http_builder

Требования:
    - Сервисы должны быть доступны.
    - Файл './testdata/files/space.jpg' должен существовать.

Пример запуска:
    python api_client_create_exercise.py
"""
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercise_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.users.user_schema import CreateUserRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.files.files_client import get_files_client
from clients.files.file_schema import CreateFileResponseSchema, CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client

"""
Клиент для публичного API пользователей. Позволяет регистрировать новых пользователей без аутентификации.
Инициализируется один раз при старте скрипта.
"""
public_users_client = get_public_users_client()

# Создаем пользователя
"""
Объект запроса на создание пользователя. Автоматически генерирует:
- Уникальный email
- Пароль (по умолчанию "string", может быть переопределён)
- Имя, фамилия и отчество (фиктивные значения)

Используется для регистрации в системе.
"""
create_user_request = CreateUserRequestSchema(
)

# Используем метод create_user
"""
Ответ от сервера после создания пользователя.

Содержит:
- user.id — уникальный идентификатор пользователя
- user.email — зарегистрированный email
- Статус аккаунта и метаданные

Этот ID будет использован как автор задания и курса.
"""
create_user_response = public_users_client.create_user(create_user_request)

"""
Объект аутентификации, содержащий учетные данные нового пользователя.

Используется для инициализации авторизованных клиентов:
- files_client
- courses_client
- exercise_client
"""
authentication_user = AuthenticationUserSchema(
    email= create_user_request.email,
    password= create_user_request.password
)
# Инициализируем клиенты
"""
Клиент для загрузки и управления файлами. Авторизован под новым пользователем.
Позволяет загружать изображения, документы и другие ресурсы.
"""
files_client = get_files_client(authentication_user)

"""
Клиент для управления курсами. Авторизован под создателем.
Позволяет создавать, редактировать и получать курсы.
"""
courses_client = get_courses_client(authentication_user)

"""
Клиент для управления заданиями. Авторизован под пользователем.
Позволяет создавать и редактировать учебные задания.
"""
exercise_client = get_exercise_client(authentication_user)

# Загружаем файл
"""
Запрос на загрузку файла. Указывает путь к локальному файлу, который будет отправлен на сервер.

Поддерживаемые форматы зависят от бэкенда (в данном случае — изображение JPG).

Файл используется как превью курса.
"""
create_file_request = CreateFileRequestSchema(upload_file='./testdata/files/space.jpg')

"""
Ответ от сервера с информацией о загруженном файле:
- file.id — идентификатор, необходимый для привязки к курсу
- file.name, file.url, file.size — метаданные

Выводится в консоль для отладки.
"""
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создаем курс
"""
Запрос на создание учебного курса.

Параметры:
- previewFileId — ID загруженного изображения
- createdByUserId — ID пользователя, который создаёт курс

Дополнительные поля (название, описание) могут быть добавлены по необходимости.
"""
create_course_request = CreateCourseRequestSchema(
    previewFileId= create_file_response.file.id,
    createdByUserId= create_user_response.user.id
)

"""
Ответ от сервера с данными созданного курса:
- course.id — используется при создании задания
- previewFileId — ссылка на обложку
- created_at, статус и др.

Выводится в консоль.
"""
create_course_response = courses_client.create_course(create_course_request)
print('Create Course data:', create_course_response)

# создаем задание
"""
Запрос на создание учебного задания.

Параметры:
- id — ID пользователя (ошибочно использован как ID задания; вероятно, должно быть сгенерировано сервером)
- course_id — ID курса, к которому привязывается задание

⚠️ Внимание: использование `id=create_user_response.user.id` может быть ошибкой.
Правильно — не передавать ID задания (пусть генерируется сервером), либо использовать корректный UUID.

Рекомендуется проверить схему `CreateExerciseRequestSchema`.
"""
create_exercise_request = CreateExerciseRequestSchema(
    id=create_user_response.user.id,
    course_id=create_course_response.course.id,
)

"""
Запрос на создание учебного задания.

Параметры:
- id — ID пользователя (ошибочно использован как ID задания; вероятно, должно быть сгенерировано сервером)
- course_id — ID курса, к которому привязывается задание

⚠️ Внимание: использование `id=create_user_response.user.id` может быть ошибкой.
Правильно — не передавать ID задания (пусть генерируется сервером), либо использовать корректный UUID.

Рекомендуется проверить схему `CreateExerciseRequestSchema`.
"""
create_exercise_response = exercise_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)

# Примечания:
#   - При каждом запуске создается новый пользователь — избегаются конфликты.
#   - Если файл не найден — выбрасывается исключение.
#   - При ошибках API (400, 401, 500) нужно добавить обработку исключений.
#   - Для продакшена рекомендуется добавить логирование и retry-логику.