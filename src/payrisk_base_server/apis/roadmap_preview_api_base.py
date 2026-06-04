# coding: utf-8

from typing import ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.account_check_request import \
    AccountCheckRequest
from payrisk_base_server.models.agent_manifest import AgentManifest
from payrisk_base_server.models.decision_resolution_request import \
    DecisionResolutionRequest
from payrisk_base_server.models.decision_resolution_response import \
    DecisionResolutionResponse
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.kyc_check_request import KycCheckRequest
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, StrictStr, field_validator
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
        x_alogram_agent_manifest: Annotated[
            Optional[AgentManifest],
            Field(
                description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
            ),
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
        x_alogram_agent_manifest: Annotated[
            Optional[AgentManifest],
            Field(
                description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
            ),
        ],
    ) -> DecisionResponse:
        """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for identity verification and KYC workflows."""
        ...

    async def resolve_decision(
        self,
        idempotency_key: Annotated[
            str,
            Field(
                min_length=3,
                max_length=128,
                description="Lowercase, prefix-free standard idempotency key to prevent duplicate capture/void.",
            ),
        ],
        tenant_id: Annotated[
            StrictStr, Field(description="The targeted Alogram Tenant ID partition.")
        ],
        decision_resolution_request: DecisionResolutionRequest,
        trace_id: Annotated[
            Optional[Annotated[str, Field()]],
            Field(
                description="Lowercase, prefix-free standard distributed trace identifier."
            ),
        ],
    ) -> DecisionResolutionResponse:
        """&gt; **Coming Soon**: This endpoint is currently in active development. Submits an administrative, human-in-the-loop, or autonomous agent decision to resolve a pending fraud review, trigger downstream payment capture/voids, and supply ground-truth feedback labels for ML model retraining."""
        ...
