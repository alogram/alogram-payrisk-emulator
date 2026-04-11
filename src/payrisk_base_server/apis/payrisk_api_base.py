# coding: utf-8

from typing import Any, ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.account_check_request import AccountCheckRequest
from payrisk_base_server.models.check_request import CheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.kyc_check_request import KycCheckRequest
from payrisk_base_server.models.payment_event import PaymentEvent
from payrisk_base_server.models.scores_success_response import ScoresSuccessResponse
from payrisk_base_server.models.signals_request import SignalsRequest
from pydantic import Field, StrictStr
from typing_extensions import Annotated


class BasePayriskApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePayriskApi.subclasses = BasePayriskApi.subclasses + (cls,)

    async def risk_check(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                strict=True,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        check_request: CheckRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> DecisionResponse: ...

    async def ingest_payment_event(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                strict=True,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        payment_event: PaymentEvent,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> None: ...

    async def ingest_signals(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                strict=True,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        signals_request: SignalsRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> None: ...

    async def get_fraud_scores(
        self,
        tenantId: Annotated[str, Field(min_length=5, strict=True, max_length=64)],
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
        x_idempotency_key: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Unique Idempotency-Key sent in the GET request etc."),
        ],
        start_time: Optional[Annotated[str, Field(strict=True)]],
        end_time: Optional[Annotated[str, Field(strict=True)]],
        page_size: Optional[Annotated[int, Field(le=500, strict=True, ge=1)]],
        page_token: Optional[StrictStr],
    ) -> ScoresSuccessResponse: ...

    async def health_check(
        self,
    ) -> None: ...

    async def account_risk_check(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                strict=True,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        account_check_request: AccountCheckRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> DecisionResponse: ...

    async def kyc_risk_check(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                strict=True,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        kyc_check_request: KycCheckRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> DecisionResponse: ...
