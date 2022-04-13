import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import (
    config,
    db,
    log,
)
import services

logger = logging.getLogger()
DEBUG = config.DEBUG
log.setup()
origins = [
    "https://yeets.me",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
serve = FastAPI(default_response_class=ORJSONResponse, debug=DEBUG)
serve.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@serve.on_event("startup")
async def startup():
    await db.start()
    await services.initialize()
    logger.debug("initialized")


@serve.on_event("shutdown")
async def shutdown():
    await db.stop()