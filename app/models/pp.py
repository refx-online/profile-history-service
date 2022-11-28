from __future__ import annotations

import datetime
from typing import Any
from typing import Mapping

from pydantic import BaseModel


class PPHistory(BaseModel):
    user_id: int
    mode: int
    captures: list

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> PPHistory:
        return cls(
            user_id=mapping["user_id"],
            mode=mapping["mode"],
            captures=[
                PPCapture.from_mapping(capture) for capture in mapping["captures"]
            ],
        )


class PPCapture(BaseModel):
    captured_at: datetime.datetime
    pp: int

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> PPCapture:
        return cls(
            captured_at=mapping["captured_at"],
            pp=mapping["pp"],
        )


# Stupid hack.
PPHistory.update_forward_refs()
