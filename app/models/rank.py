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
            captures=[RankCapture.from_mapping(rank) for rank in mapping["captures"]],
        )


class RankCapture(BaseModel):
    captured_at: datetime.datetime
    overall: int
    country: int | None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> RankCapture:
        return cls(
            captured_at=mapping["captured_at"],
            overall=mapping["rank"],
            country=mapping["c_rank"],
        )


class RankPeak(BaseModel):
    user_id: int
    mode: int
    captured_at: datetime.datetime
    rank: int

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> RankPeak:
        return cls(
            user_id=mapping["user_id"],
            mode=mapping["mode"],
            captured_at=mapping["captured_at"],
            rank=mapping["rank"],
        )


# Stupid hack.
RankHistory.update_forward_refs()
