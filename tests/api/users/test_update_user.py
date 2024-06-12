from typing import Annotated

from allure import feature, title
from pytest import mark, fixture

from api.custom_request import MethodEnum
from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import CreateUserDto
from other.random_values import get_random_job, get_random_name
from tests.allure_constants import AllureApiUsers


@feature('Обновить пользователя PATCH/PUT /api/users')
class TestUpdateUser(AllureApiUsers):

    @title('Частично обновить пользователя')
    @mark.bug
    @mark.xfail
    def test_patch_user(self, fixture_create_user: Annotated[CreateUserDto, fixture]):
        response = ReqresUsers().update_user(
            method=MethodEnum.PATCH,
            user_id=fixture_create_user.id_,
            json={'name': get_random_name()}
        )

        response.assert_status_code(expected_code=200)
        response.assert_model_valid()

    @title('Обновить пользователя')
    def test_put_user(self, fixture_create_user: Annotated[CreateUserDto, fixture]):
        response = ReqresUsers().update_user(
            method=MethodEnum.PUT,
            user_id=fixture_create_user.id_,
            json={'name': get_random_name(), 'job': get_random_job()}
        )

        response.assert_status_code(expected_code=200)
        response.assert_model_valid()
