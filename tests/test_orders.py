import allure

from conftest import BASE_URL


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_authorized(self, api_session, auth_headers, valid_ingredients):
        response = api_session.post(
            f"{BASE_URL}/orders",
            headers=auth_headers,
            json={"ingredients": valid_ingredients},
            timeout=20,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)

    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_unauthorized(self, api_session, valid_ingredients):
        response = api_session.post(
            f"{BASE_URL}/orders",
            json={"ingredients": valid_ingredients},
            timeout=20,
        )

        assert response.status_code == 401

    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients(self, api_session, auth_headers):
        response = api_session.post(
            f"{BASE_URL}/orders",
            headers=auth_headers,
            json={"ingredients": []},
            timeout=20,
        )

        assert response.status_code == 400
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided",
        }

    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_invalid_ingredient_hash(self, api_session, auth_headers):
        response = api_session.post(
            f"{BASE_URL}/orders",
            headers=auth_headers,
            json={"ingredients": ["invalid-ingredient-hash"]},
            timeout=20,
        )

        assert response.status_code == 500

