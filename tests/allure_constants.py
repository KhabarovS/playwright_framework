from allure import epic
from pytest import mark


@epic('Users')
@mark.api
class AllureApiUsers:
    """ Разметка сервиса Users """
    ...


@epic('Resource')
@mark.api
class AllureApiResource:
    """ Разметка сервиса Resource """
    ...


@epic('Register')
@mark.api
class AllureApiRegister:
    """ Разметка сервиса Register """
    ...


@epic('Login')
@mark.api
class AllureApiLogin:
    """ Разметка сервиса Login """
    ...


@epic('UI')
@mark.web
class AllureWebUi:
    """ Разметка сервиса UI """
    ...
