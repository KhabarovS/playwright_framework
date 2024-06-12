from allure import feature, title
from pytest import mark

from api.services.reqres_in.login import ReqresLogin
from dto.login_dto import LoginResponse
from dto.register_dto import RegisterResponse
from other.random_values import get_random_email, get_random_string
from tests.allure_constants import AllureApiLogin


@feature('Проверить метод логина пользователя')
class TestLoginUser(AllureApiLogin):

    @title('Логин пользователя с валидными данными')
    def test_login_user(self):
        response_obj = ReqresLogin().post_login(
            json={'email': 'eve.holt@reqres.in', 'password': 'cityslicka'},
            response_model=LoginResponse,
        )

        response_obj.raise_for_status()
        response_obj.assert_model_valid()

    @title('[-] Логин пользователя с невалидными данными')
    @mark.parametrize(
        'json, msg', [
            ({'email': get_random_email()}, 'Missing password'),
            ({'password': get_random_string()}, 'Missing email or username'),
            ({}, 'Missing email or username')
        ]
    )
    def test_login_user_unsuccessful(self, json: dict, msg: str):
        response = ReqresLogin().post_login(json=json, response_model=RegisterResponse)

        response.assert_status_code(expected_code=400)
        response.assert_model_valid()
        assert msg == response.json()['error']
