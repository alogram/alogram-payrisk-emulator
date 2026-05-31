# coding: utf-8

from typing import ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from payrisk_base_server.models.problem import Problem
from payrisk_base_server.models.scores_success_response import \
    ScoresSuccessResponse
from payrisk_base_server.security_api import get_token_ApiKey, get_token_oAuth2
from pydantic import Field, StrictStr, field_validator
from typing_extensions import Annotated


class BaseForensicDataApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseForensicDataApi.subclasses = BaseForensicDataApi.subclasses + (cls,)

    async def get_fraud_scores(
        self,
        tenantId: Annotated[str, Field(min_length=6, max_length=68)],
        x_trace_id: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Echoed or generated trace ID for tracking requests."),
        ],
        x_idempotency_key: Annotated[
            Optional[Annotated[str, Field(min_length=36, max_length=36)]],
            Field(description="Unique Idempotency-Key sent in the GET request etc."),
        ],
        start_time: Optional[Annotated[str, Field()]],
        end_time: Optional[Annotated[str, Field()]],
        page_size: Optional[Annotated[int, Field(le=500, ge=1)]],
        page_token: Optional[StrictStr],
    ) -> ScoresSuccessResponse: ...
