class DataProvider:
    """
    Класс-провайдер тестовых данных для параметризованных API-тестов.

    Содержит статические методы, возвращающие наборы данных
    для позитивных и негативных сценариев авторизации.
    Используется совместно с @pytest.mark.parametrize.

    Автор: Деревянченко Николай Николаевич
    """

    @staticmethod
    def getAuthDataPositive():
        """
        Возвращает набор корректных учётных данных для позитивного
        сценария авторизации.

        Каждый элемент списка — кортеж вида (email, password),
        для которого ожидается успешная авторизация (статус 200,
        наличие токена в ответе).

        Returns:
            list[tuple[str, str]]: список кортежей (email, password)
                с валидными учётными данными.

        Пример использования:
            @pytest.mark.parametrize(
                "email, password",
                DataProvider.getAuthDataPositive()
            )
            def testAuthPositive(email, password):
                ...
        """
        return [
            (
                "eve.holt@reqres.in",
                "cityslicka"
            )
        ]

    @staticmethod
    def getAuthDataNegative():
        """
        Возвращает набор некорректных учётных данных для негативного
        сценария авторизации.

        Каждый элемент списка — кортеж вида (email, password),
        для которого ожидается ошибка авторизации (статус 400,
        сообщение об ошибке в ответе, отсутствие токена).

        Текущий кейс: валидный email с пустым паролем —
        проверка обработки отсутствующего обязательного поля password.

        Returns:
            list[tuple[str, str]]: список кортежей (email, password)
                с невалидными учётными данными.

        Пример использования:
            @pytest.mark.parametrize(
                "email, password",
                DataProvider.getAuthDataNegative()
            )
            def testAuthNegative(email, password):
                ...
        """
        return [
            (
                "eve.holt@reqres.in",
                ""
            )
        ]