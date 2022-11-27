from __future__ import annotations

import datetime
from typing import Any
from typing import Mapping

from pydantic import BaseModel


class CountryRankHistory(BaseModel):
    user_id: int
    mode: int
    captures: list[CountryRankCapture]

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> CountryRankHistory:
        return cls(
            user_id=mapping["user_id"],
            mode=mapping["mode"],
            captures=[
                CountryRankCapture.from_mapping(capture)
                for capture in mapping["captures"]
            ],
        )


class CountryRankCapture(BaseModel):
    captured_at: datetime.datetime
    value: int

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> CountryRankCapture:
        return cls(
            captured_at=mapping["captured_at"],
            value=mapping["c_rank"],
        )


# Stupid hack.
CountryRankHistory.update_forward_refs()
