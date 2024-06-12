from typing import Type

from allure import dynamic, feature, step
from pydantic import BaseModel
from pytest import mark

from api.custom_request import MethodEnum
from api.services.reqres_in.login import ReqresLogin
from api.services.reqres_in.register import ReqresRegister
from api.services.reqres_in.unknown import ReqresUnknown
from api.services.reqres_in.users import ReqresUsers
from dto.login_dto import LoginResponse
from dto.register_dto import RegisterResponse
from dto.unknown_dto import ResourceListResponseDto, ResourceSingleResponseDto
from dto.users_dto import RequestUserDto, UserResponseDto, UsersListResponseDto
from tests.allure_constants import AllureWebUi
from tests.api.conftest import get_request_to_reqres
from web.pages.reqres_in.main_page import MainPage, RequestEnum

TEST_DATA = [
    (
        (ReqresUsers().get_users, {'params': {'page': 2}}, UsersListResponseDto),
        RequestEnum.LIST_USERS,
        UsersListResponseDto
    ),
    (
        (ReqresUsers().get_single_user, {'user_id': 2}, UserResponseDto),
        RequestEnum.SINGLE_USERS,
        UserResponseDto
    ),
    (
        (ReqresUsers().get_single_user, {'user_id': 23}, UserResponseDto),
        RequestEnum.SINGLE_USER_NOT_FOUND,
        UserResponseDto
    ),
    (
        (ReqresUnknown().get_unknown_list, {}, ResourceListResponseDto),
        RequestEnum.LIST_RESOURCE,
        ResourceListResponseDto
    ),
    (
        (ReqresUnknown().get_single_unknown, {'resource_id': 2}, ResourceSingleResponseDto),
        RequestEnum.SINGLE_RESOURCE,
        ResourceSingleResponseDto

    ),
    (
        (ReqresUnknown().get_single_unknown, {'resource_id': 23}, ResourceSingleResponseDto),
        RequestEnum.SINGLE_RESOURCE_NOT_FOUND,
        ResourceSingleResponseDto
    ),
    (
        (ReqresUsers().create_user, {'json': {'name': 'morpheus', 'job': 'leader'}}, RequestUserDto),
        RequestEnum.CREATE_USER,
        RequestUserDto
    ),
    (
        (
            ReqresUsers().update_user,
            {'method': MethodEnum.PUT, 'json': {'name': 'morpheus', 'job': 'zion resident'}, 'user_id': 2},
            RequestUserDto
        ),
        RequestEnum.PUT_UPDATE_USER,
        RequestUserDto
    ),
    (
        (
            ReqresUsers().update_user,
            {'method': MethodEnum.PATCH, 'json': {'name': 'morpheus', 'job': 'zion resident'}, 'user_id': 2},
            RequestUserDto
        ),
        RequestEnum.PATCH_UPDATE_USER,
        RequestUserDto
    ),
    (
        (ReqresUsers().delete_user, {'user_id': 2}, None),
        RequestEnum.DELETE_USER,
        None
    ),
    (
        (
            ReqresRegister().post_register,
            {'json': {'email': 'eve.holt@reqres.in', 'password': 'pistol'}},
            RegisterResponse
        ),
        RequestEnum.REGISTER_SUCCESSFUL,
        RegisterResponse
    ),
    (
        (ReqresRegister().post_register, {'json': {'email': 'sydney@fife'}}, RegisterResponse),
        RequestEnum.REGISTER_UNSUCCESSFUL,
        RegisterResponse
    ),
    (
        (ReqresLogin().post_login, {'json': {'email': 'eve.holt@reqres.in', 'password': 'cityslicka'}}, LoginResponse),
        RequestEnum.LOGIN_SUCCESSFUL,
        LoginResponse
    ),
    (
        (ReqresLogin().post_login, {'json': {'email': 'peter@klaven'}}, LoginResponse),
        RequestEnum.LOGIN_UNSUCCESSFUL,
        LoginResponse
    ),
    (
        (ReqresUsers().get_users, {'params': {'delay': 3}}, UsersListResponseDto),
        RequestEnum.DELAY,
        UsersListResponseDto
    )
]


@feature('Проверить корректность отправленных запросов UI и API')
class TestUIResponseBody(AllureWebUi):
    MSG_CODE = 'Статус код UI "{ui_code}" не равен коду с API "{api_code}"'
    MSG_BODY = 'Тело ответа UI "{ui_body}" не равен телу ответа с API "{api_body}"'

    @mark.parametrize('open_page', [MainPage], indirect=True)
    @mark.parametrize('get_request_to_reqres, name_request, model', TEST_DATA, indirect=['get_request_to_reqres'])
    def test_ui_response_body(
            self,
            open_page: MainPage,
            get_request_to_reqres: tuple,
            name_request: RequestEnum,
            model: Type[BaseModel]
    ):
        dynamic.title(f'Проверить ответ метода {name_request.value}')
        api_code, api_body = get_request_to_reqres

        with step('Нажать на кнопку отправки запроса и ожидание ответа'):
            open_page.click_by_request(name_request=name_request)
            open_page.find_element_by_locator(locator=open_page.LOAD_SPINNER_HIDE)

        with step('Сравнить код ответа отображенный на UI и код ответа API'):
            ui_code = int(open_page.find_element_by_locator(locator=open_page.RESPONSE_STATUS_CODE).text_content())
            assert ui_code == api_code, self.MSG_CODE.format(ui_code=ui_code, api_code=api_code)

        with step('Сравнить тело ответа отображенный на UI и тело ответа API'):
            text_element = open_page.find_element_by_locator(locator=open_page.RESPONSE_BODY).text_content()

            ui_body = model.model_validate_json(text_element) if text_element else None
            assert ui_body == api_body, self.MSG_BODY.format(ui_body=ui_body, api_body=api_body)
