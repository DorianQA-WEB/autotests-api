import httpx

# Проходим аутентификацию
login_payload = {
    "email": "user@example.com",
    "password": "string"
}
login_response = httpx.post("https://reqres.in/api-docs/#/default/post_login", json=login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)

# Инициализируем клиент с авторизацией
client = httpx.Client(
    base_url="https://localhost:8000",
    timeout=100,
    headers={"Authorization": f"Bearer {login_response_data['token']['accessToken']}"}
)

# Выполняем запрос с авторизацией
get_user_me_response = client.get("api/get/users/me")
get_user_me_response_data = get_user_me_response.json()
print('Get user me data:', get_user_me_response_data)