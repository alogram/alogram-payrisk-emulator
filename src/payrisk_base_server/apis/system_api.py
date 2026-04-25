# This file is auto-generated. Do not modify manually.
# coding: utf-8

import importlib
import pkgutil
from typing import Any, Dict, List  # noqa: F401

import payrisk_base_server.impl
from fastapi import (APIRouter, Body, Cookie, Depends, Form,  # noqa: F401
                     Header, HTTPException, Path, Query, Response, Security,
                     status)
from payrisk_base_server.apis.system_api_base import BaseSystemApi
from payrisk_base_server.models.extra_models import TokenModel  # noqa: F401

router = APIRouter()

ns_pkg = payrisk_base_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v1/health",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unavailable"},
    },
    tags=["System"],
    summary="Health check for the service",
    response_model_by_alias=True,
)
async def health_check() -> None:
    if not BaseSystemApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSystemApi.subclasses[0]().health_check()
