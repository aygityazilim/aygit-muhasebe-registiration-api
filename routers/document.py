from fastapi import APIRouter, Response, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List
from shared.enums import StatusCodeEnum
from shared.schemas import ResponseSchema
from services.document import DocumentService, UPLOAD_DIR
from dependencies import get_document_service
import os

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


@router.get("/uploads/{tracking_number}/{filename}")
async def serve_file(tracking_number: str, filename: str):
    file_path = os.path.join(UPLOAD_DIR, tracking_number, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı.")
    return FileResponse(file_path)
