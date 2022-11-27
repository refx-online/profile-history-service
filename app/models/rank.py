from __future__ import annotations

import datetime
from typing import Any
from typing import Mapping

from pydantic import BaseModel

from app.models.c_rank import CountryRankCapture


class MixedRankHistory(BaseModel):
    global_rank: list[RankCapture]
    country_rank: list[CountryRankCapture]

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> MixedRankHistory:
        return cls(
            global_rank=[
                RankCapture.from_mapping(capture) for capture in mapping["global_rank"]
            ],
            country_rank=[
                CountryRankCapture.from_mapping(capture)
                for capture in mapping["country_rank"]
            ],
        )


class RankHistory(BaseModel):
    user_id: int
    mode: int
    captures: MixedRankHistory

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> RankHistory:

        return cls(
            user_id=mapping["user_id"],
            mode=mapping["mode"],
            captures=MixedRankHistory.from_mapping(mapping["captures"]),
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
MixedRankHistory.update_forward_refs()
