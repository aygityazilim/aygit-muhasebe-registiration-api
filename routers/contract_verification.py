from fastapi import APIRouter, Response, Depends, Query
from shared.enums import StatusCodeEnum
from shared.schemas import ResponseSchema
from services.contract_verification import ContractVerificationService
from dependencies import get_contract_verification_service

router = APIRouter(
    prefix="/contract-verification",
    tags=["Registiration Contract Verification"]
)


@router.patch("/{tracking_number}/send-code")
async def send_code(
    response: Response,
    tracking_number: str,
    contract: int = Query(...),
    service: ContractVerificationService = Depends(get_contract_verification_service)
):
    await service.send_code(tracking_number, contract)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=None)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.patch("/{tracking_number}/verify-code")
async def verify_code(
    response: Response,
    tracking_number: str,
    contract: int = Query(...),
    code: str = Query(...),
    service: ContractVerificationService = Depends(get_contract_verification_service)
):
    await service.verifiy_code(tracking_number, contract, code)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=None)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data
