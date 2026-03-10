from fastapi import APIRouter, Response, Depends, UploadFile, File
from typing import Optional, List
from shared.enums import StatusCodeEnum
from shared.schemas import ResponseSchema
from services.document import DocumentService
from dependencies import get_document_service

router = APIRouter(
    prefix="/documents",
    tags=["Registiration Documents"]
)


@router.post("/{tracking_number}")
async def upload_documents(
    response: Response,
    tracking_number: str,
    tax_plate: Optional[UploadFile] = File(None),
    other: List[UploadFile] = File(default=[]),
    service: DocumentService = Depends(get_document_service)
):
    data = await service.upload(tracking_number, tax_plate, other)
    result = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return result
