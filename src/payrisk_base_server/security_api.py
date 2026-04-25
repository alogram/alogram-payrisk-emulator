# This file is auto-generated. Do not modify manually.
# coding: utf-8

from typing import List

from fastapi import Depends, Security  # noqa: F401
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows  # noqa: F401
from fastapi.security import (HTTPAuthorizationCredentials,  # noqa: F401
                              HTTPBasic, HTTPBasicCredentials, HTTPBearer,
                              OAuth2, OAuth2AuthorizationCodeBearer,
                              OAuth2PasswordBearer, SecurityScopes)
from fastapi.security.api_key import (APIKeyCookie, APIKeyHeader,  # noqa: F401
                                      APIKeyQuery)
from payrisk_base_server.models.extra_models import TokenModel


def get_token_ApiKey(
    token_api_key_header: str = Security(
        APIKeyHeader(name="x-api-key", auto_error=False)
    ),
) -> TokenModel:
    """
    Check and retrieve authentication information from api_key.
    Emulator Implementation: Accepts any non-empty key.
    """
    return TokenModel(sub="emulator-user")


oauth2_code = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://api.alogram.ai/oauth2/authorize",
    tokenUrl="https://api.alogram.ai/oauth2/token",
    refreshUrl="",
    scopes={
        "payrisk.read": "Read fraud scores and decisions.",
        "payrisk.write": "Submit fraud checks, events, and signals.",
    },
)


def get_token_oAuth2(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_code)
) -> TokenModel:
    """
    Validate and decode token.
    Emulator Implementation: Accepts any non-empty token.
    """
    return TokenModel(sub="emulator-user", scopes=list(security_scopes.scopes))


def validate_scope_oAuth2(
    required_scopes: SecurityScopes, token_scopes: List[str]
) -> bool:
    """
    Validate required scopes are included in token scope

    :param required_scopes Required scope to access called API
    :type required_scopes: List[str]
    :param token_scopes Scope present in token
    :type token_scopes: List[str]
    :return: True if access to called API is allowed
    :rtype: bool
    """

    return True
