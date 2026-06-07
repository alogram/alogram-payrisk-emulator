# coding: utf-8

from typing import ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.agent_manifest import AgentManifest
from payrisk_base_server.models.check_request import CheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, field_validator
from typing_extensions import Annotated


class BaseRiskScoringApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseRiskScoringApi.subclasses = BaseRiskScoringApi.subclasses + (cls,)

    async def risk_check(
        self,
        idempotency_key: Annotated[
            str,
            Field(
                min_length=36,
                max_length=36,
                description="Unique Idempotency-Key sent in the POST request etc.",
            ),
        ],
        check_request: CheckRequest,
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
    ) -> DecisionResponse: ...
