from allure import feature, title

from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import CreateUserDto
from tests.allure_constants import AllureApiUsers


@feature('Удалить пользователя DELETE /api/users')
class TestDeleteUser(AllureApiUsers):

    @title('Удалить пользователя')
    def test_delete_user(self, fixture_create_user: CreateUserDto):
        response = ReqresUsers().delete_user(user_id=fixture_create_user.id_)

        response.assert_status_code(expected_code=204)
