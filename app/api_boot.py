from __future__ import annotations

from app.api.rest import init_api
from app.common import logger

logger.configure_logging()

api = init_api()
