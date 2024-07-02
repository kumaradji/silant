# silant/adapters.py

from allauth.account.adapter import DefaultAccountAdapter


class NoSignupAccountAdapter(DefaultAccountAdapter):
    """
    Класс NoSignupAccountAdapter используется для отключения возможности регистрации новых пользователей через интерфейс allauth.
    Наследует класс DefaultAccountAdapter из пакета allauth.
    """

    def is_open_for_signup(self, request):
        """
        Метод is_open_for_signup переопределяет поведение метода регистрации пользователей.
        Возвращает False, что означает отключение возможности регистрации новых пользователей.

        :param request: Объект запроса Django
        :return: False
        """
        return False
