import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from utils import (
    config,
    db,
    log,
)
import services

logger = logging.getLogger()
DEBUG = config.DEBUG
log.setup()
serve = FastAPI(default_response_class=ORJSONResponse, debug=DEBUG)


@serve.on_event("startup")
async def startup():
    await db.start()
    await services.initialize()
    logger.debug("initialized")


@serve.on_event("shutdown")
async def shutdown():
    await db.stop()