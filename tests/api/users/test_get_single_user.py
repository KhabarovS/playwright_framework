from allure import feature, title
from pytest import mark, param

from api.services.reqres_in.users import ReqresUsers
from tests.allure_constants import AllureApiUsers


@feature('Проверить метод получения пользователей GET /api/users/{user_id}')
class TestGetSingleUser(AllureApiUsers):

    @title('Получить пользователя с валидными параметрами')
    @mark.parametrize('user_id', [1, 2])
    def test_get_single_user(self, user_id: int):
        response = ReqresUsers().get_single_user(user_id=user_id)

        response.raise_for_status()
        response.assert_model_valid()

    @title('Получить пользователя с валидными параметрами NOT FOUND')
    @mark.parametrize('user_id', [23, 55])
    def test_get__user_not_found(self, user_id: int):
        response = ReqresUsers().get_single_user(user_id=user_id)

        response.assert_status_code(expected_code=404)
        assert '{}' == response.text, f'Тело ответа "{response.text}" не соответствует ожидаемому {{}}'

    @title('[-] Получить пользователя невалидным идентификатором')
    @mark.parametrize(
        'user_id', [
            param('один', marks=mark.bug),
            param(0, marks=mark.bug),
            param(-1, marks=mark.bug)
        ]
    )
    @mark.xfail(reason='Баг')
    def test_get_users_list_negative(self, user_id: int):
        response = ReqresUsers().get_single_user(user_id=user_id)

        response.assert_status_code(expected_code=400)
