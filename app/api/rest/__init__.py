from __future__ import annotations

import logging
import time

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import RequestResponseEndpoint

from app.common import settings
from app.services import database
from app.services import redis


def init_db(api: FastAPI) -> None:
    @api.on_event("startup")
    async def startup_db() -> None:
        logging.info("Starting up database pool")
        database_service = database.Database(
            read_dsn="mysql+asyncmy://{username}:{password}@{host}:{port}/{db}".format(
                username=settings.READ_DB_USER,
                password=settings.READ_DB_PASS,
                host=settings.READ_DB_HOST,
                port=settings.READ_DB_PORT,
                db=settings.READ_DB_NAME,
            ),
            write_dsn="mysql+asyncmy://{username}:{password}@{host}:{port}/{db}".format(
                username=settings.WRITE_DB_USER,
                password=settings.WRITE_DB_PASS,
                host=settings.WRITE_DB_HOST,
                port=settings.WRITE_DB_PORT,
                db=settings.WRITE_DB_NAME,
            ),
        )
        await database_service.connect()
        api.state.db = database_service
        logging.info("Database pool started up")

    @api.on_event("shutdown")
    async def shutdown_db() -> None:
        logging.info("Shutting down database pool")
        await api.state.db.disconnect()
        del api.state.db
        logging.info("Database pool shut down")


def init_redis(api: FastAPI) -> None:
    @api.on_event("startup")
    async def startup_redis() -> None:
        logging.info("Starting up redis pool")
        service_redis = redis.ServiceRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASS,
            ssl=settings.REDIS_USE_SSL,
            username=settings.REDIS_USER,
        )
        await service_redis.initialize()  # type: ignore[unused-awaitable]
        api.state.redis = service_redis
        logging.info("Redis pool started up")

    @api.on_event("shutdown")
    async def shutdown_redis() -> None:
        logging.info("Shutting down the redis")
        await api.state.redis.close()
        del api.state.redis
        logging.info("Redis pool shut down")


def init_middlewares(api: FastAPI) -> None:
    @api.middleware("http")
    async def add_db_to_request(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request.state.db = request.app.state.db
        response = await call_next(request)
        return response

    @api.middleware("http")
    async def add_redis_to_request(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request.state.redis = request.app.state.redis
        response = await call_next(request)
        return response

    @api.middleware("http")
    async def add_process_time_header(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.perf_counter_ns()
        response = await call_next(request)
        process_time = (time.perf_counter_ns() - start_time) / 1e6
        response.headers["X-Process-Time"] = str(process_time)  # ms
        return response


def init_routes(api: FastAPI) -> None:
    from .v1 import router as v1_router

    api.include_router(v1_router)


def init_api() -> FastAPI:
    api = FastAPI()

    init_db(api)
    init_redis(api)
    init_middlewares(api)
    init_routes(api)
    return api
