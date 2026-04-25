# coding: utf-8

import importlib
import pkgutil
from typing import Any, Dict, List, Optional  # noqa: F401

import payrisk_base_server.impl
from fastapi import (APIRouter, Body, Cookie, Depends, Form,  # noqa: F401
                     Header, HTTPException, Path, Query, Response, Security,
                     status)
from payrisk_base_server.apis.signal_intelligence_api_base import \
    BaseSignalIntelligenceApi
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401
from payrisk_base_server.models.payment_event import PaymentEvent
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.models.signals_request import SignalsRequest
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, field_validator
from typing_extensions import Annotated

router = APIRouter()

ns_pkg = payrisk_base_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


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
    tags=["Signal Intelligence"],
    summary="Ingest Lifecycle Signals",
    response_model_by_alias=True,
)
async def ingest_payment_event(
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
    payment_event: PaymentEvent = Body(None, description=""),
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
) -> None:
    if not BaseSignalIntelligenceApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSignalIntelligenceApi.subclasses[0]().ingest_payment_event(
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
    tags=["Signal Intelligence"],
    summary="Submit Behavioral Intelligence",
    response_model_by_alias=True,
)
async def ingest_signals(
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
    signals_request: SignalsRequest = Body(None, description=""),
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
) -> None:
    if not BaseSignalIntelligenceApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSignalIntelligenceApi.subclasses[0]().ingest_signals(
        x_idempotency_key, signals_request, x_trace_id
    )
