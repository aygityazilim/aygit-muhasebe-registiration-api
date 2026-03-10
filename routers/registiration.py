from fastapi import APIRouter, Request, Response, Depends
from shared.enums import StatusCodeEnum
from shared.schemas import (
    ResponseSchema,
    RegistirationCreateSchema
)
from services.registiration import RegistirationService
from dependencies import get_registiration_service

router  = APIRouter(
    prefix="",
    tags=["Registiration"]
)

@router.post("/")
async def create(
    request: Request,
    response: Response,
    payload: RegistirationCreateSchema,
    service: RegistirationService = Depends(get_registiration_service)
):
    data = await service.create(payload)
    data = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return data

@router.get("/{number}")
async def get_one(
    request: Request,
    response: Response,
    number: str,
    service: RegistirationService = Depends(get_registiration_service)
):
    data = await service.get_one(number)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data