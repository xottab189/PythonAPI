"""
Модуль общих pytest-фикстур для API-тестов.

Содержит фикстуры, доступные во всех тестах проекта через conftest.py
или прямой импорт.

Автор: Деревянченко Николай Николаевич
"""

import pytest

import config


@pytest.fixture(scope="session")
def headers_data():
    """
    Формирует заголовки для HTTP-запросов к API.

    Заголовки включают тип содержимого запроса и API-ключ,
    необходимый для аутентификации всех запросов к reqres.in.
    Значения берутся из модуля конфигурации config.

    Scope: session — фикстура создаётся один раз за всю сессию
    тестирования и переиспользуется во всех тестах, так как
    заголовки не изменяются между запросами.

    Returns:
        dict: словарь заголовков вида
            {
                "Content-Type": <тип содержимого>,
                "x-api-key": <API-ключ>
            }

    Пример использования:
        def testAuthPositive(headers_data, email, password):
            response = requests.post(
                url,
                json={"email": email, "password": password},
                headers=headers_data
            )
    """
    return {'Content-Type': config.contentType, 'x-api-key': config.token}
