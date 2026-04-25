# This file is auto-generated. Do not modify manually.
# coding: utf-8

from typing import Any, ClassVar, Dict, List, Tuple  # noqa: F401


class BaseSystemApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSystemApi.subclasses = BaseSystemApi.subclasses + (cls,)

    async def health_check(
        self,
    ) -> None: ...
