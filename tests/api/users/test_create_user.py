from typing import Annotated

from allure import feature, title
from pytest import mark, param, fixture

from api.services.reqres_in.users import ReqresUsers
from other.random_values import get_random_job, get_random_name
from tests.allure_constants import AllureApiUsers


@feature('Создать пользователя POST /api/users')
class TestCreateUser(AllureApiUsers):

    @title('Создать пользователя с валидными параметрами')
    def test_create_user(self, fixture_delete_user: Annotated[list, fixture]):
        response = ReqresUsers().create_user(json={'name': get_random_name(), 'job': get_random_job()})

        response.assert_status_code(expected_code=201)

        fixture_delete_user.append(response.json()['id'])

        response.assert_model_valid()

    @title('[-] Создать пользователя с не валидными параметрами')
    @mark.parametrize(
        'json', [
            param({'name': '', 'job': get_random_job()}, marks=mark.bug),
            param({'name': get_random_name(), 'job': ''}, marks=mark.bug),
            param({'name': get_random_name()}, marks=mark.bug),
            param({'job': get_random_job()}, marks=mark.bug),
        ]
    )
    @mark.xfail
    def test_create_user_negative(self, json: dict[str, str], fixture_delete_user: Annotated[list, fixture]):
        response = ReqresUsers().create_user(json=json)

        if str(response.status_code)[0] == '2':
            fixture_delete_user.append(response.json()['id'])

        response.assert_status_code(expected_code=400)
