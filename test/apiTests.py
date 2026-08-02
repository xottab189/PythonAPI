"""
Модуль API-тестов для сервиса reqres.in.

Покрывает:
    - позитивный и негативный сценарии авторизации (задание 2.2);
    - получение списка пользователей и проверку уникальности
      аватаров (задание 2.1).

Автор: Деревянченко Николай Николаевич
"""

import allure
import pytest
import requests

from config import BASE_URL
from src.helpers.DataProvider import DataProvider
from src.pojo.Dto import ResourceDto


@pytest.mark.parametrize(
   "email, password",
    DataProvider.getAuthDataPositive()
)
def testAuthPositive(email, password, headers_data):
    """
    Проверяет успешную авторизацию пользователя с валидными
    email и паролем.

    Ожидаемый результат: в теле ответа присутствует непустой токен.

    Автор: Деревянченко Николай Николаевич

    Args:
        email (str): email пользователя, передаётся через parametrize.
        password (str): пароль пользователя, передаётся через parametrize.
        headers_data (dict): заголовки запроса, фикстура из conftest.py.
    """
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
    """
    Проверяет отказ в авторизации при отсутствии пароля.

    Ожидаемый результат: статус-код 400, в теле ответа присутствует
    сообщение об ошибке, токен отсутствует.

    Автор: Деревянченко Николай Николаевич

    Args:
        headers_data (dict): заголовки запроса, фикстура из conftest.py.
        email (str): email пользователя, передаётся через parametrize.
        password (str): пароль пользователя (пустой), передаётся через parametrize.
    """
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
    """
    Получает список пользователей с указанной страницы и проверяет,
    что URL аватаров всех пользователей уникальны.

    Ответ API парсится в объект ResourceDto — если структура ответа
    не соответствует ожидаемой схеме, тест упадёт на этапе парсинга
    с понятной ошибкой валидации Pydantic.

    Автор: Деревянченко Николай Николаевич

    Args:
        headers_data (dict): заголовки запроса, фикстура из conftest.py.
        page (int): номер страницы пользователей, передаётся через parametrize.
    """
    with allure.step(f"Получение списка пользователей со страницы {page}"):
        response = requests.get(f"{BASE_URL}/users?page={page}", headers=headers_data)

    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )

    with allure.step("Парсинг ответа в объект ResourceDto"):
        resource = ResourceDto(**response.json())
        assert len(resource.data) > 0, "Список пользователей пуст"

    with allure.step("Проверка уникальности avatar"):
        avatars = [user.avatar for user in resource.data]
        assert len(avatars) == len(set(avatars)), (
            f"Найдены дублирующиеся avatar: {avatars}"
        )