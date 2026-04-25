# coding: utf-8

import importlib
import pkgutil
from typing import Dict, List, Optional  # noqa: F401

import payrisk_base_server.impl
from fastapi import (APIRouter, Body, Cookie, Depends, Form,  # noqa: F401
                     Header, HTTPException, Path, Query, Response, Security,
                     status)
from payrisk_base_server.apis.forensic_data_api_base import BaseForensicDataApi
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401
from payrisk_base_server.models.problem import Problem
from payrisk_base_server.models.scores_success_response import \
    ScoresSuccessResponse
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, StrictStr, field_validator
from typing_extensions import Annotated

router = APIRouter()

ns_pkg = payrisk_base_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


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
    tags=["Forensic Data"],
    summary="Query Historical Assessments",
    response_model_by_alias=True,
)
async def get_fraud_scores(
    tenantId: Annotated[str, Field(min_length=5, max_length=64)] = Path(
        ...,
        description="",
        regex=r"^tid_[a-z0-9\-_]{2,60}$",
        min_length=5,
        max_length=64,
    ),
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
    x_idempotency_key: Annotated[
        Optional[Annotated[str, Field(min_length=36, max_length=36)]],
        Field(description="Unique Idempotency-Key sent in the GET request etc."),
    ] = Header(
        None,
        description="Unique Idempotency-Key sent in the GET request etc.",
        regex=r"^idk_[a-f0-9]{32}$",
        min_length=36,
        max_length=36,
    ),
    start_time: Optional[Annotated[str, Field()]] = Query(
        None,
        description="",
        alias="startTime",
        regex=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$",
    ),
    end_time: Optional[Annotated[str, Field()]] = Query(
        None,
        description="",
        alias="endTime",
        regex=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$",
    ),
    page_size: Optional[Annotated[int, Field(le=500, ge=1)]] = Query(
        50, description="", alias="pageSize", ge=1, le=500
    ),
    page_token: Optional[StrictStr] = Query(None, description="", alias="pageToken"),
) -> ScoresSuccessResponse:
    if not BaseForensicDataApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseForensicDataApi.subclasses[0]().get_fraud_scores(
        tenantId,
        x_trace_id,
        x_idempotency_key,
        start_time,
        end_time,
        page_size,
        page_token,
    )
