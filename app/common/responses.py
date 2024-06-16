from __future__ import annotations

from typing import Any
from typing import Generic
from typing import Literal
from typing import TypeVar

from pydantic import BaseModel

from app.common import json
from app.common.errors import ServiceError

T = TypeVar("T")


class Success(BaseModel, Generic[T]):
    status: Literal["success"]
    data: T


def success(
    content: Any,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
) -> json.ORJSONResponse:
    data = {"status": "success", "data": content}
    return json.ORJSONResponse(data, status_code, headers)


class ErrorResponse(BaseModel):
    status: Literal["error"]
    error: ServiceError
    message: str


def failure(
    error: ServiceError,
    message: str,
    status_code: int = 400,
    headers: dict[str, str] | None = None,
) -> json.ORJSONResponse:
    data = {"status": "error", "error": error, "message": message}
    return json.ORJSONResponse(data, status_code, headers)
