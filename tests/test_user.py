import allure
import pytest

from conftest import BASE_URL


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUserUpdate:
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Авторизованный пользователь может изменить поле: {field}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_any_field_authorized(self, api_session, registered_user, auth_headers, field):
        values = {
            "email": f"updated-{registered_user['email']}",
            "password": "NewPassword123!",
            "name": "Updated API User",
        }

        response = api_session.patch(
            f"{BASE_URL}/auth/user",
            headers=auth_headers,
            json={field: values[field]},
            timeout=20,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True

        # Для password НЕ проверяем значение в ответе (его там нет)
        if field != "password":
            assert body["user"][field] == values[field], f"Поле {field} не обновилось корректно"

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Неавторизованный пользователь не может изменить поле: {field}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_any_field_unauthorized(self, api_session, field):
        values = {
            "email": "anonymous@example.com",
            "password": "NewPassword123!",
            "name": "Anonymous User",
        }
        response = api_session.patch(
            f"{BASE_URL}/auth/user",
            json={field: values[field]},
            timeout=20,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
