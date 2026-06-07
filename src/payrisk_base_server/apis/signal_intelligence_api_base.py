# coding: utf-8

from typing import ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.agent_manifest import AgentManifest
from payrisk_base_server.models.ingest_payment_event202_response import \
    IngestPaymentEvent202Response
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
        idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        payment_event: PaymentEvent,
        trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
        alogram_agent_manifest: Annotated[
            Optional[AgentManifest],
            Field(
                description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
            ),
        ],
    ) -> IngestPaymentEvent202Response: ...

    async def ingest_signals(
        self,
        idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        signals_request: SignalsRequest,
        trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
        alogram_agent_manifest: Annotated[
            Optional[AgentManifest],
            Field(
                description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
            ),
        ],
    ) -> IngestPaymentEvent202Response: ...
