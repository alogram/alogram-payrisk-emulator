# coding: utf-8

from typing import ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.account_check_request import \
    AccountCheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.kyc_check_request import KycCheckRequest
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, field_validator
from typing_extensions import Annotated


class BaseRoadmapPreviewApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseRoadmapPreviewApi.subclasses = BaseRoadmapPreviewApi.subclasses + (cls,)

    async def account_risk_check(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        account_check_request: AccountCheckRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> DecisionResponse:
        """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for account-level events such as signup, login, and profile changes."""
        ...

    async def kyc_risk_check(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        kyc_check_request: KycCheckRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> DecisionResponse:
        """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for identity verification and KYC workflows."""
        ...
