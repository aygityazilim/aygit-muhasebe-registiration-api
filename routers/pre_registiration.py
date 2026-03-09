from fastapi import APIRouter, Request, Response, Depends
from shared.enums import StatusCodeEnum
from shared.schemas import (
    ResponseSchema,
    PreRegistirationCreateSchema
)
from services.pre_registiration import PreRegistirationService
from dependencies import get_pre_registiration_service

router  = APIRouter(
    prefix="",
    tags=["Pre Registiration"]
)

@router.get("/{tracking_number}")
async def get_one(
    request: Request,
    response: Response,
    tracking_number: str,
    service: PreRegistirationService = Depends(get_pre_registiration_service)
):
    data = await service.get_one(tracking_number)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.post("/")
async def create(
    request: Request,
    response: Response,
    payload: PreRegistirationCreateSchema,
    service: PreRegistirationService = Depends(get_pre_registiration_service)
):
    data = await service.create(payload)
    data = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return data