import allure

from conftest import BASE_URL


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов конкретного пользователя")
class TestUserOrders:
    @allure.title("Авторизованный пользователь получает свои заказы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_orders_authorized(self, api_session, auth_headers):
        response = api_session.get(
            f"{BASE_URL}/orders",
            headers=auth_headers,
            timeout=20,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["orders"], list)
        assert "total" in body
        assert "totalToday" in body

    @allure.title("Неавторизованный пользователь не получает свои заказы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_orders_unauthorized(self, api_session):
        response = api_session.get(f"{BASE_URL}/orders", timeout=20)

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
