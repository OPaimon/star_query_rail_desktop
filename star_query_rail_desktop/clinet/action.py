from star_query_rail_client import AuthenticatedClient, Client
from star_query_rail_client.api.account import (
    register_account_account_signup_post,
    update_password_account_me_password_patch,
)
from star_query_rail_client.api.login import (
    login_access_token_login_access_token_post,
    test_token_login_test_token_post,
)
from star_query_rail_client.api.user import (
    bind_user_user_post,
    get_characters_detail_user_get_post,
    get_info_user_get_info_get,
    unbind_user_user_unbind_userid_delete,
)
from star_query_rail_client.models import (
    BodyLoginAccessTokenLoginAccessTokenPost,
    ConnectUCRegister,
    Email,
    EmailBase,
    EmailRegister,
    EmailUpdate,
    EUCPublic,
    HTTPValidationError,
    Message,
    StarRailDetailCharacters,
    Token,
    UserCreate,
)

from .config import settings, status


def register(email: str, password: str) -> Email:
    with Client(base_url=settings.API_url) as client:
        body = EmailRegister(email=email, psw=password)
        response: Email = register_account_account_signup_post.sync(
            client=client, body=body
        )
    return response


def update_password(password: str) -> Message:
    with AuthenticatedClient(base_url=settings.API_url, token=status.token) as client:
        body = EmailUpdate(psw=password)
        response: Message = update_password_account_me_password_patch.sync(
            client=client, body=body
        )
    return response


def get_info():
    with AuthenticatedClient(base_url=settings.API_url, token=status.token) as client:
        response: EUCPublic = get_info_user_get_info_get.sync(client=client)
    status.email = response.email
    status.userid = response.userid
    status.character = response.characters
    return response


def login(username: str, password: str) -> AuthenticatedClient:
    with Client(base_url=settings.API_url) as client:
        body = BodyLoginAccessTokenLoginAccessTokenPost(username, password)
        response: Token = login_access_token_login_access_token_post.sync(
            client=client, body=body
        )
    authenticated_client = AuthenticatedClient(
        base_url=settings.API_url, token=response.access_token
    )
    status.token = response.access_token
    return authenticated_client


def logout():
    status.token = None
    status.email = None
    status.userid = None
    status.character = None


def bind_cookies(cookies: str) -> EUCPublic | HTTPValidationError:
    if status.token:
        with AuthenticatedClient(
            base_url=settings.API_url, token=status.token
        ) as client:
            user_create = UserCreate(cookie=cookies)
            response: EUCPublic = bind_user_user_post.sync(
                client=client, body=user_create
            )
        print(type(response))
        if type(response) is EUCPublic:
            status.userid = response.userid
            status.character = response.characters
        return response


def unbind_user() -> Message:
    if status.token:
        with AuthenticatedClient(
            base_url=settings.API_url, token=status.token
        ) as client:
            response = unbind_user_user_unbind_userid_delete.sync(
                client=client, userid=status.userid
            )
        return response


def get_characters_detail(index: int == 0) -> StarRailDetailCharacters | None:
    if status.token and status.character:
        body = ConnectUCRegister(cid=status.character[index].cid, userid=status.userid)
        with AuthenticatedClient(
            base_url=settings.API_url, token=status.token
        ) as client:
            response = get_characters_detail_user_get_post.sync(
                client=client, body=body
            )
        return response
    return None
