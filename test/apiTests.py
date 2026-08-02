

import allure
import pytest
import requests

from config import BASE_URL
from src.helpers import DataProvider

@pytest.mark.parametrize(
   "email, password",
    DataProvider.getAuthDataPositive()
)
def testAuthPositive(email, password, headers_data):
    with allure.step("Проверка авторизации (позитивный сценарий)"):
        response = requests.post(
            f"{BASE_URL}/login",
            json={"email": email, "password": password},
            headers = headers_data
        )

    with allure.step("Проверка тела ответа"):
        body = response.json()
        assert "token" in body, "В ответе отсутствует поле token"
        assert body["token"], "Токен пустой"


@pytest.mark.parametrize(
     "email, password",
     DataProvider.getAuthDataNegative()
)
def testAuthNegative(headers_data, email, password ):
    response = requests.post(
            f"{BASE_URL}/login",
            json={"email": email, "password": password},
            headers = headers_data
        )
    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 400, (
            f"Ожидался статус 400, получен {response.status_code}"
        )
    with allure.step("Проверка тела ответа"):
        body = response.json()
        assert "error" in body, "В ответе отсутствует поле error"
        assert body["error"], "Сообщение об ошибке пустое"
        assert "token" not in body, "Токен не должен присутствовать при неуспешной авторизации"


@pytest.mark.parametrize("page", [2])
def testGetAvatarAndCheckName(headers_data, page):
    with allure.step(f"Получение списка пользователей со страницы {page}"):
        response = requests.get(f"{BASE_URL}/users?page={page}", headers=headers_data)

    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )

    with allure.step("Проверка тела ответа"):
        body = response.json()
        assert "data" in body, "В ответе отсутствует поле data"
        assert len(body["data"]) > 0, "Список пользователей пуст"

    with allure.step("Проверка наличия avatar у каждого пользователя"):
        avatars = [user.get("avatar") for user in body["data"]]
        assert all(avatars), "У одного или нескольких пользователей отсутствует avatar"

    with allure.step("Проверка уникальности avatar"):
        assert len(avatars) == len(set(avatars)), (
            f"Найдены дублирующиеся avatar: {avatars}"
        )