from fastapi import Request

from app.common.context import Context
from app.services import database
from app.services import redis


class RequestContext(Context):
    def __init__(self, request: Request) -> None:
        self.request = request

    @property
    def db(self) -> database.Database:
        return self.request.state.db

    @property
    def redis(self) -> redis.ServiceRedis:
        return self.request.state.redis
