# coding: utf-8

import importlib
import pkgutil
from typing import Dict, List, Optional  # noqa: F401

import payrisk_base_server.impl
from fastapi import (APIRouter, Body, Cookie, Depends, Form,  # noqa: F401
                     Header, HTTPException, Path, Query, Response, Security,
                     status)
from payrisk_base_server.apis.roadmap_preview_api_base import \
    BaseRoadmapPreviewApi
from payrisk_base_server.models.account_check_request import \
    AccountCheckRequest
from payrisk_base_server.models.agent_manifest import AgentManifest
from payrisk_base_server.models.decision_resolution_request import \
    DecisionResolutionRequest
from payrisk_base_server.models.decision_resolution_response import \
    DecisionResolutionResponse
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401
from payrisk_base_server.models.kyc_check_request import KycCheckRequest
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, StrictStr, field_validator
from typing_extensions import Annotated

router = APIRouter()

ns_pkg = payrisk_base_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v1/risk/account/check",
    responses={
        200: {"model": DecisionResponse, "description": "Synchronous risk decision."},
        400: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        429: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["Roadmap &amp; Preview"],
    summary="Synchronous fraud decision for account/session events",
    response_model_by_alias=True,
)
async def account_risk_check(
    x_idempotency_key: Annotated[
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
    account_check_request: AccountCheckRequest = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        regex=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    x_alogram_agent_manifest: Annotated[
        Optional[AgentManifest],
        Field(
            description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
        ),
    ] = Header(
        None,
        description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). ",
    ),
) -> DecisionResponse:
    """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for account-level events such as signup, login, and profile changes."""
    if not BaseRoadmapPreviewApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRoadmapPreviewApi.subclasses[0]().account_risk_check(
        x_idempotency_key, account_check_request, x_trace_id, x_alogram_agent_manifest
    )


@router.post(
    "/v1/risk/kyc/check",
    responses={
        200: {"model": DecisionResponse, "description": "Synchronous risk decision."},
        400: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        429: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["Roadmap &amp; Preview"],
    summary="Synchronous decision for KYC/identity verification",
    response_model_by_alias=True,
)
async def kyc_risk_check(
    x_idempotency_key: Annotated[
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
    kyc_check_request: KycCheckRequest = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        regex=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    x_alogram_agent_manifest: Annotated[
        Optional[AgentManifest],
        Field(
            description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). "
        ),
    ] = Header(
        None,
        description="JSON-encoded AgentManifest for autonomous shopping agents.  Required for machine-to-machine trust validation (UCP/MCP). ",
    ),
) -> DecisionResponse:
    """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for identity verification and KYC workflows."""
    if not BaseRoadmapPreviewApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRoadmapPreviewApi.subclasses[0]().kyc_risk_check(
        x_idempotency_key, kyc_check_request, x_trace_id, x_alogram_agent_manifest
    )


@router.post(
    "/v1/decisions",
    responses={
        200: {
            "model": DecisionResolutionResponse,
            "description": "Decision successfully resolved and persisted to state ledger.",
        },
        400: {"model": Problem, "description": "An error response."},
        401: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["Roadmap &amp; Preview"],
    summary="Resolve Review (Assisted Decisioning &amp; ML Feedback)",
    response_model_by_alias=True,
)
async def resolve_decision(
    idempotency_key: Annotated[
        str,
        Field(
            min_length=3,
            max_length=128,
            description="Lowercase, prefix-free standard idempotency key to prevent duplicate capture/void.",
        ),
    ] = Header(
        None,
        description="Lowercase, prefix-free standard idempotency key to prevent duplicate capture/void.",
        min_length=3,
        max_length=128,
    ),
    tenant_id: Annotated[
        StrictStr, Field(description="The targeted Alogram Tenant ID partition.")
    ] = Header(None, description="The targeted Alogram Tenant ID partition."),
    decision_resolution_request: DecisionResolutionRequest = Body(None, description=""),
    trace_id: Annotated[
        Optional[Annotated[str, Field()]],
        Field(
            description="Lowercase, prefix-free standard distributed trace identifier."
        ),
    ] = Header(
        None,
        description="Lowercase, prefix-free standard distributed trace identifier.",
        regex=r"^trc_[a-f0-9]{32}$",
    ),
) -> DecisionResolutionResponse:
    """&gt; **Coming Soon**: This endpoint is currently in active development. Submits an administrative, human-in-the-loop, or autonomous agent decision to resolve a pending fraud review, trigger downstream payment capture/voids, and supply ground-truth feedback labels for ML model retraining."""
    if not BaseRoadmapPreviewApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRoadmapPreviewApi.subclasses[0]().resolve_decision(
        idempotency_key, tenant_id, decision_resolution_request, trace_id
    )
