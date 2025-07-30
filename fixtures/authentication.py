from clients.authentication.authentication_client import get_authentication_client, AuthenticationClient
import pytest



@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()


