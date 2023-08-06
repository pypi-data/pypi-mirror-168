from unittest.mock import patch

import pytest

from sym.flow.cli.errors import InvalidTokenError
from sym.flow.cli.helpers.login.login_flow import LoginError, PasswordPromptFlow
from sym.flow.cli.models import UserCredentials
from sym.flow.cli.tests.conftest import get_mock_response

PASSWORD_PROMPT_PATH = "sym.flow.cli.helpers.login.login_flow.PasswordPromptFlow"


@pytest.fixture
def password_prompt_flow(mocker):
    return PasswordPromptFlow()


@pytest.fixture
def user_creds():
    return UserCredentials("username", "password")


def test_login_with_user_creds(
    global_options, password_prompt_flow, user_creds, test_org
):
    response = get_mock_response(
        status_code=200,
        data={
            "access_token": "test-access-token",
            "token_type": "Bearer",
            "expires_in": "86400",
            "refresh_token": "test-refresh-token",
            "scope": "test-scope offline_access",
        },
    )

    with patch("requests.post", return_value=response) as mock_post:
        token = password_prompt_flow.login_with_user_creds(
            global_options,
            user_creds,
            test_org,
        )

    mock_post.assert_called_once_with(
        "https://auth.com/oauth/token",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "realm": "Username-Password-Authentication",
            "username": "username",
            "password": "password",
            "audience": "https://api.com",
            "scope": "admin offline_access",
            "client_id": test_org.client_id,
        },
    )

    assert token["access_token"] == "test-access-token"
    assert token["refresh_token"] == "test-refresh-token"


def test_login_with_user_creds_no_refresh_token(
    global_options, password_prompt_flow, user_creds, test_org
):
    with pytest.raises(InvalidTokenError):
        response = get_mock_response(
            status_code=200,
            data={
                "access_token": "test-access-token",
                "token_type": "Bearer",
                "expires_in": "86400",
                "scope": "test-scope offline_access",
            },
        )

        with patch("requests.post", return_value=response):
            password_prompt_flow.login_with_user_creds(
                global_options,
                user_creds,
                test_org,
            )


def test_login_with_user_creds_error_response(
    global_options, password_prompt_flow, user_creds, test_org
):
    with pytest.raises(LoginError):
        with patch("requests.post", return_value=get_mock_response(status_code=403)):
            password_prompt_flow.login_with_user_creds(
                global_options,
                user_creds,
                test_org,
            )


def test_login(global_options, password_prompt_flow, user_creds, auth_token, test_org):
    with patch(
        f"{PASSWORD_PROMPT_PATH}.prompt_for_user_credentials", return_value=user_creds
    ) as mock_prompt:
        with patch(
            f"{PASSWORD_PROMPT_PATH}.login_with_user_creds", return_value=auth_token
        ) as mock_login:
            token = password_prompt_flow.login(global_options, test_org)

    assert token == auth_token
    mock_prompt.assert_called_once()
    mock_login.assert_called_once_with(global_options, user_creds, test_org)
