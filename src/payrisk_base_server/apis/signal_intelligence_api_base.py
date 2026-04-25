# coding: utf-8

from typing import Any, ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.payment_event import PaymentEvent
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.models.signals_request import SignalsRequest
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, field_validator
from typing_extensions import Annotated


class BaseSignalIntelligenceApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSignalIntelligenceApi.subclasses = BaseSignalIntelligenceApi.subclasses + (
            cls,
        )

    async def ingest_payment_event(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        payment_event: PaymentEvent,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> None: ...

    async def ingest_signals(
        self,
        x_idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        signals_request: SignalsRequest,
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
    ) -> None: ...
