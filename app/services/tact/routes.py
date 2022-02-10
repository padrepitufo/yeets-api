import logging
from typing import Optional

from fastapi import APIRouter, Header
from pydantic import BaseModel

from services.tact import models
from services import BaseSerializer

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/tacts",
    tags=["tacts"],
    dependencies=[],
)



class TactCreationRequest(BaseModel):
    tact_type_id: str
    args: str


class TactTypeCreationRequest(BaseModel):
    name: str
    params: str
    tact_type_id: str | None = None


class TactConfirmationRequestCreationRequest(BaseModel):
    tact_id: str


class TactConfirmationCreationRequest(BaseModel):
    request_id: str


class Serializer(BaseSerializer):
    data: list[models.TactData]


class SerializerTactType(BaseSerializer):
    data: list[models.TactTypeData]


class SerializerTactConfirmationRequest(BaseSerializer):
    data: list[models.TactConfirmationRequestData]


class SerializerTactConfirmation(BaseSerializer):
    data: list[models.TactConfirmationData]


@router.get("/", response_model=Serializer)
async def tacts(tact_id: Optional[str] = None):
    data = await models.tact_listing(tact_id=tact_id)
    return Serializer(data=data)


@router.post("/", response_model=Serializer)
async def create_tact(item: TactCreationRequest):
    data = await models.tact_create(
        tact_type_id=item.tact_type_id,
        args=item.args,
    )
    return Serializer(data=[data])


@router.get("/types", response_model=SerializerTactType)
async def tact_types(tact_type_id: Optional[str] = None):
    data = await models.tact_type_listing(tact_type_id=tact_type_id)
    return SerializerTactType(data=data)


@router.post("/types", response_model=SerializerTactType)
async def create_tact_type(item: TactTypeCreationRequest):
    data = await models.tact_type_create(
        name=item.name,
        params=item.params,
        tact_type_id=item.tact_type_id,
    )
    return SerializerTactType(data=[data])


@router.get(
    "/confirmations",
    response_model=SerializerTactConfirmation,
)
async def tact_confirmations(request_id: str):
    data = await models.tact_confirmation_listing(request_id=request_id)
    return SerializerTactConfirmation(data=data)


@router.post(
    "/confirmations",
    response_model=SerializerTactConfirmation,
)
async def create_tact_confirmation(item: TactConfirmationCreationRequest, user_agent: Optional[str] = Header(None)):
    data = await models.tact_confirmation_create(
        meta_data=user_agent,
        request_id=item.request_id,
    )
    return SerializerTactConfirmation(data=[data])


@router.get(
    "/confirmations/requests",
    response_model=SerializerTactConfirmationRequest,
)
async def tact_confirmation_requests(tact_id: Optional[str] = None):
    data = await models.tact_confirmation_request_listing(tact_id=tact_id)
    return SerializerTactConfirmationRequest(data=data)


@router.post(
    "/confirmations/requests",
    response_model=SerializerTactConfirmationRequest,
)
async def create_tact_confirmation_request(item: TactConfirmationRequestCreationRequest):
    data = await models.tact_confirmation_request_create(tact_id=item.tact_id)
    return SerializerTactConfirmationRequest(data=[data])
