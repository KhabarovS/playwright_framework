from allure import feature, title
from pytest import mark, param

from api.services.reqres_in.users import ReqresUsers
from tests.allure_constants import AllureApiUsers


@feature('Проверить метод получения списка пользователей GET /api/users')
class TestGetUsersList(AllureApiUsers):

    @title('Получить список пользователей с валидными параметрами')
    @mark.parametrize('page', [1, 2])
    def test_get_users_list(self, page: int):
        response = ReqresUsers().get_users(params={'page': page})

        response.raise_for_status()
        response.assert_model_valid()

    @title('Получить список пользователей с ожиданием')
    @mark.parametrize('delay', [1, 2, 3])
    def test_get_user_list_with_delay(self, delay: int):
        response = ReqresUsers().get_users(params={'delay': delay})

        response.raise_for_status()
        response.assert_model_valid()

    @title('[-] Получить список с невалидными параметрами')
    @mark.parametrize(
        'page', [
            param('один', marks=mark.bug),
            param(0, marks=mark.bug),
            param(-1, marks=mark.bug)
        ]
    )
    @mark.xfail(reason='Баг')
    def test_get_users_list_negative(self, page: str):
        response = ReqresUsers().get_users(params={'page': page})

        response.assert_status_code(expected_code=400)
