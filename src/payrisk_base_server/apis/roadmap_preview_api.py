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
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401
from payrisk_base_server.models.kyc_check_request import KycCheckRequest
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, field_validator
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
) -> DecisionResponse:
    """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for account-level events such as signup, login, and profile changes."""
    if not BaseRoadmapPreviewApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRoadmapPreviewApi.subclasses[0]().account_risk_check(
        x_idempotency_key, account_check_request, x_trace_id
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
) -> DecisionResponse:
    """&gt; **Coming Soon**: This endpoint is currently in active development. Assess risk for identity verification and KYC workflows."""
    if not BaseRoadmapPreviewApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRoadmapPreviewApi.subclasses[0]().kyc_risk_check(
        x_idempotency_key, kyc_check_request, x_trace_id
    )
