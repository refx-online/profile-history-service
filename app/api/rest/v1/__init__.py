from __future__ import annotations

from fastapi import APIRouter

from . import pp
from . import rank


router = APIRouter(prefix="/api/v1/profile-history")

router.include_router(rank.router, tags=["rank"])
router.include_router(pp.router, tags=["pp"])
