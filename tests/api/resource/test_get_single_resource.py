from allure import feature, title
from pytest import mark, param

from api.services.reqres_in.unknown import ReqresUnknown
from tests.allure_constants import AllureApiResource


@feature('Проверить метод получения ресурса GET /api/unknown/{resource_id}')
class TestGetSingleResource(AllureApiResource):

    @title('Получить ресурс с валидными параметрами')
    @mark.parametrize('resource_id', [1, 2])
    def test_get_resource_user(self, resource_id: int):
        response = ReqresUnknown().get_single_unknown(resource_id=resource_id)

        response.raise_for_status()
        response.assert_model_valid()

    @title('Получить ресурс с валидными параметрами NOT FOUND')
    @mark.parametrize('resource_id', [23, 55])
    def test_get__user_not_found(self, resource_id: int):
        response = ReqresUnknown().get_single_unknown(resource_id=resource_id)

        response.assert_status_code(expected_code=404)
        assert '{}' == response.text, f'Тело ответа "{response.text}" не соответствует ожидаемому {{}}'

    @title('[-] Получить ресурс невалидным идентификатором')
    @mark.parametrize(
        'resource_id', [
            param('один', marks=mark.bug),
            param(0, marks=mark.bug),
            param(-1, marks=mark.bug)
        ]
    )
    @mark.xfail(reason='Баг')
    def test_get_users_list_negative(self, resource_id: int):
        response = ReqresUnknown().get_single_unknown(resource_id=resource_id)

        response.assert_status_code(expected_code=400)
