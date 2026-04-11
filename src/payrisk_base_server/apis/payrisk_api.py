# coding: utf-8

import importlib
import pkgutil
from typing import Any, Dict, List, Optional  # noqa: F401

import payrisk_base_server.impl
from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)
from payrisk_base_server.apis.payrisk_api_base import BasePayriskApi
from payrisk_base_server.models.account_check_request import AccountCheckRequest
from payrisk_base_server.models.check_request import CheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401
from payrisk_base_server.models.kyc_check_request import KycCheckRequest
from payrisk_base_server.models.payment_event import PaymentEvent
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.models.scores_success_response import ScoresSuccessResponse
from payrisk_base_server.models.signals_request import SignalsRequest
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, StrictStr
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
    tags=["payrisk"],
    summary="Synchronous fraud decision for a purchase",
    response_model_by_alias=True,
)
async def risk_check(
    x_idempotency_key: Annotated[
        str,
        Field(
            min_length=36,
            strict=True,
            max_length=36,
            description="Unique Idempotency-Key sent in the POST request etc.",
        ),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the POST request etc.",
        pattern=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    check_request: CheckRequest = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        pattern=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    token_ApiKey: TokenModel = Security(get_token_ApiKey),
    token_oAuth2: TokenModel = Security(get_token_oAuth2, scopes=["payrisk.write"]),
) -> DecisionResponse:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().risk_check(
        x_idempotency_key, check_request, x_trace_id
    )


@router.post(
    "/v1/events",
    responses={
        202: {"description": "Accepted"},
        400: {"model": Problem, "description": "An error response."},
        401: {"model": Problem, "description": "An error response."},
        403: {"model": Problem, "description": "An error response."},
        404: {"model": Problem, "description": "An error response."},
        409: {"model": Problem, "description": "An error response."},
        413: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        429: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["payrisk"],
    summary="Ingest payment lifecycle events (authorization, capture, settlement, refund, dispute, chargeback, chargeback_outcome). ",
    response_model_by_alias=True,
)
async def ingest_payment_event(
    x_idempotency_key: Annotated[
        str,
        Field(
            min_length=36,
            strict=True,
            max_length=36,
            description="Unique Idempotency-Key sent in the POST request etc.",
        ),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the POST request etc.",
        pattern=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    payment_event: PaymentEvent = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        pattern=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    token_ApiKey: TokenModel = Security(get_token_ApiKey),
    token_oAuth2: TokenModel = Security(get_token_oAuth2, scopes=["payrisk.write"]),
) -> None:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().ingest_payment_event(
        x_idempotency_key, payment_event, x_trace_id
    )


@router.post(
    "/v1/signals",
    responses={
        202: {"description": "Accepted"},
        400: {"model": Problem, "description": "An error response."},
        413: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        429: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["payrisk"],
    summary="Ingest non-payment signals (account or interaction) for modeling",
    response_model_by_alias=True,
)
async def ingest_signals(
    x_idempotency_key: Annotated[
        str,
        Field(
            min_length=36,
            strict=True,
            max_length=36,
            description="Unique Idempotency-Key sent in the POST request etc.",
        ),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the POST request etc.",
        pattern=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    signals_request: SignalsRequest = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        pattern=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    token_ApiKey: TokenModel = Security(get_token_ApiKey),
    token_oAuth2: TokenModel = Security(get_token_oAuth2, scopes=["payrisk.write"]),
) -> None:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().ingest_signals(
        x_idempotency_key, signals_request, x_trace_id
    )


@router.get(
    "/v1/scores/{tenantId}",
    responses={
        200: {
            "model": ScoresSuccessResponse,
            "description": "List of fraud scores for a customer.",
        },
        400: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["payrisk"],
    summary="Retrieve fraud scores for a customer",
    response_model_by_alias=True,
)
async def get_fraud_scores(
    tenantId: Annotated[str, Field(min_length=5, strict=True, max_length=64)] = Path(
        ...,
        description="",
        pattern=r"^tid_[a-z0-9_-]{2,60}$",
        min_length=5,
        max_length=64,
    ),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        pattern=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    x_idempotency_key: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Unique Idempotency-Key sent in the GET request etc."),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the GET request etc.",
        pattern=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    start_time: Optional[Annotated[str, Field(strict=True)]] = Query(
        None,
        description="",
        alias="startTime",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$",
    ),
    end_time: Optional[Annotated[str, Field(strict=True)]] = Query(
        None,
        description="",
        alias="endTime",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$",
    ),
    page_size: Optional[Annotated[int, Field(le=500, strict=True, ge=1)]] = Query(
        50, description="", alias="pageSize", ge=1, le=500
    ),
    page_token: Optional[StrictStr] = Query(None, description="", alias="pageToken"),
    token_ApiKey: TokenModel = Security(get_token_ApiKey),
    token_oAuth2: TokenModel = Security(get_token_oAuth2, scopes=["payrisk.read"]),
) -> ScoresSuccessResponse:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().get_fraud_scores(
        tenantId,
        x_trace_id,
        x_idempotency_key,
        start_time,
        end_time,
        page_size,
        page_token,
    )


@router.get(
    "/v1/health",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unavailable"},
    },
    tags=["payrisk"],
    summary="Health check for the service",
    response_model_by_alias=True,
)
async def health_check() -> None:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().health_check()


@router.post(
    "/v1/risk/account/check",
    responses={
        200: {"model": DecisionResponse, "description": "Synchronous risk decision."},
        400: {"model": Problem, "description": "An error response."},
        422: {"model": Problem, "description": "An error response."},
        429: {"model": Problem, "description": "An error response."},
        500: {"model": Problem, "description": "An error response."},
    },
    tags=["payrisk"],
    summary="Synchronous fraud decision for account/session events (signup, login, settings)",
    response_model_by_alias=True,
)
async def account_risk_check(
    x_idempotency_key: Annotated[
        str,
        Field(
            min_length=36,
            strict=True,
            max_length=36,
            description="Unique Idempotency-Key sent in the POST request etc.",
        ),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the POST request etc.",
        pattern=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    account_check_request: AccountCheckRequest = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        pattern=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    token_ApiKey: TokenModel = Security(get_token_ApiKey),
    token_oAuth2: TokenModel = Security(get_token_oAuth2, scopes=["payrisk.write"]),
) -> DecisionResponse:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().account_risk_check(
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
    tags=["payrisk"],
    summary="Synchronous decision for KYC/identity verification",
    response_model_by_alias=True,
)
async def kyc_risk_check(
    x_idempotency_key: Annotated[
        str,
        Field(
            min_length=36,
            strict=True,
            max_length=36,
            description="Unique Idempotency-Key sent in the POST request etc.",
        ),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the POST request etc.",
        pattern=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    kyc_check_request: KycCheckRequest = Body(None, description=""),
    x_trace_id: Annotated[
        Optional[Annotated[str, Field(min_length=36, strict=True, max_length=36)]],
        Field(description="Echoed or generated trace ID for tracking requests."),
    ] = Header(
        None,
        description="Echoed or generated trace ID for tracking requests.",
        pattern=r"^trc_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    token_ApiKey: TokenModel = Security(get_token_ApiKey),
    token_oAuth2: TokenModel = Security(get_token_oAuth2, scopes=["payrisk.write"]),
) -> DecisionResponse:
    if not BasePayriskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayriskApi.subclasses[0]().kyc_risk_check(
        x_idempotency_key, kyc_check_request, x_trace_id
    )
