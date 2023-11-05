from __future__ import annotations

import atexit

import app.exception_handling
from app.api.rest import init_api
from app.common import logger

logger.configure_logging()
app.exception_handling.hook_exception_handlers()
atexit.register(app.exception_handling.unhook_exception_handlers)


api = init_api()
