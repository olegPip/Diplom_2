import allure
import pytest

from conftest import BASE_URL


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserRegistration:
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_unique_user(self, api_session, new_user):
        response = api_session.post(f"{BASE_URL}/auth/register", json=new_user, timeout=20)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == new_user["email"]
        assert body["user"]["name"] == new_user["name"]
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Регистрация уже зарегистрированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_existing_user(self, api_session, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"],
        }
        response = api_session.post(f"{BASE_URL}/auth/register", json=payload, timeout=20)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "User already exists",
        }

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Регистрация без обязательного поля: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_without_required_field(self, api_session, new_user, missing_field):
        payload = new_user.copy()
        payload[missing_field] = ""

        response = api_session.post(f"{BASE_URL}/auth/register", json=payload, timeout=20)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields",
        }


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLogin:
    @allure.title("Логин под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, api_session, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }
        response = api_session.post(f"{BASE_URL}/auth/login", json=payload, timeout=20)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == registered_user["email"]
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @pytest.mark.parametrize(
        "email,password",
        [
            ("wrong@example.com", "TestPassword123!"),
            ("{valid_email}", "WrongPassword123!"),
        ],
    )
    @allure.title("Логин с неверными учётными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_credentials(self, api_session, registered_user, email, password):
        email = registered_user["email"] if email == "{valid_email}" else email
        response = api_session.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=20,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }
