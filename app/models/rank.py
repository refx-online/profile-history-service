from __future__ import annotations

import datetime
from typing import Any
from typing import Mapping

from pydantic import BaseModel


class RankHistory(BaseModel):
    user_id: int
    mode: int
    captures: list[RankCapture]

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> RankHistory:
        return cls(
            user_id=mapping["user_id"],
            mode=mapping["mode"],
            captures=[
                RankCapture.from_mapping(capture) for capture in mapping["captures"]
            ],
        )


class RankCapture(BaseModel):
    captured_at: datetime.datetime
    value: int

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> RankCapture:
        return cls(
            captured_at=mapping["captured_at"],
            value=mapping["rank"],
        )


# Stupid hack.
RankHistory.update_forward_refs()
