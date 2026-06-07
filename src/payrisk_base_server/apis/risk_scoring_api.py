# coding: utf-8

import importlib
import pkgutil
from typing import Dict, List, Optional  # noqa: F401

import payrisk_base_server.impl
from fastapi import (APIRouter, Body, Cookie, Depends, Form,  # noqa: F401
                     Header, HTTPException, Path, Query, Response, Security,
                     status)
from payrisk_base_server.apis.risk_scoring_api_base import BaseRiskScoringApi
from payrisk_base_server.models.agent_manifest import AgentManifest
from payrisk_base_server.models.check_request import CheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, field_validator
from typing_extensions import Annotated

router = APIRouter()

ns_pkg = payrisk_base_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v1/risk/check",
    responses={
        200: {"model": DecisionResponse, "description": "Synchronous risk decision."},
        400: {"model": Problem, "description": "An error response."},
        401: {"model": Problem, "description": "An error response."},
        403: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        429: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["Risk Scoring"],
    summary="Assess Transaction Risk",
    response_model_by_alias=True,
)
async def risk_check(
    idempotency_key: Annotated[
        str,
        Field(
            min_length=36,
            max_length=36,
            description="Unique Idempotency-Key sent in the POST request etc.",
        ),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the POST request etc.",
        regex=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    check_request: CheckRequest = Body(None, description=""),
    trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        regex=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    alogram_agent_manifest: Annotated[
        Optional[AgentManifest],
        Field(
            description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
        ),
    ] = Header(
        None,
        description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). ",
    ),
) -> DecisionResponse:
    if not BaseRiskScoringApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRiskScoringApi.subclasses[0]().risk_check(
        idempotency_key, check_request, trace_id, alogram_agent_manifest
    )
