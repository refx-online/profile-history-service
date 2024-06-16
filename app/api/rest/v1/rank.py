from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.rank import RankHistory
from app.models.rank import RankPeak
from app.usecases import rank
from app.usecases import user
from app.usecases import validation

router = APIRouter()


@router.get("/rank", response_model=Success[RankHistory])
async def get_profile_rank_history(
    user_id: int,
    mode: int,
    ctx: RequestContext = Depends(),
) -> Response:
    data = await rank.fetch_many(ctx, user_id, mode)
    user_data = await user.fetch_one(ctx, user_id, mode)

    if isinstance(user_data, ServiceError):
        return responses.failure(
            user_data,
            "Failed to fetch user data.",
            status_code=200,
        )

    if validation.is_restricted(user_data.privileges):
        return responses.failure(
            ServiceError.USERS_IS_RESTRICTED,
            "User is restricted.",
            status_code=200,
        )

    if validation.is_not_active(user_data.latest_pp_awarded):
        return responses.failure(
            ServiceError.USERS_IS_NOT_ACTIVE,
            "User is not active.",
            status_code=200,
        )

    # get current rank to create in real time rank history.
    current_rank_capture = await rank.fetch_current(
        ctx,
        user_id,
        mode,
        user_data.country,
    )

    if not current_rank_capture:
        return responses.failure(
            ServiceError.RANKS_NOT_FOUND,
            "Failed to fetch newest rank capture.",
            status_code=200,
        )

    data.captures.append(current_rank_capture)
    return responses.success(data)


@router.get("/peak-rank", response_model=Success[RankPeak])
async def get_profile_peak_rank(
    user_id: int,
    mode: int,
    ctx: RequestContext = Depends(),
) -> Response:
    data = await rank.fetch_peak(ctx, user_id, mode)
    user_data = await user.fetch_one(ctx, user_id, mode)

    if isinstance(user_data, ServiceError):
        return responses.failure(
            user_data,
            "Failed to fetch user data.",
            status_code=200,
        )

    if validation.is_restricted(user_data.privileges):
        return responses.failure(
            ServiceError.USERS_IS_RESTRICTED,
            "User is restricted.",
            status_code=200,
        )

    if validation.is_not_active(user_data.latest_pp_awarded):
        return responses.failure(
            ServiceError.USERS_IS_NOT_ACTIVE,
            "User is not active.",
            status_code=200,
        )

    if isinstance(data, ServiceError):
        return responses.failure(
            data,
            "Failed to fetch peak rank.",
            status_code=200,
        )

    # get current rank to create in real time rank peak.
    current_rank_data = await rank.fetch_current_rank(
        ctx,
        user_id,
        mode,
    )

    if not current_rank_data:
        return responses.failure(
            ServiceError.RANKS_NOT_FOUND,
            "Failed to fetch newest rank data.",
            status_code=200,
        )

    if current_rank_data.rank < data.rank:
        data = current_rank_data

    return responses.success(data)
