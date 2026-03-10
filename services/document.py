import os
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from shared.repositories import RegistirationRepository, DocumentRepository
from shared.schemas import DocumentResponseSchema
from shared.enums import StatusCodeEnum
from typing import Optional, List


UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.registiration_repository = RegistirationRepository(db=db)
        self.document_repository = DocumentRepository(db=db)

    def _save_file(self, tracking_number: str, file: UploadFile) -> str:
        folder = os.path.join(UPLOAD_DIR, tracking_number)
        os.makedirs(folder, exist_ok=True)
        ext = os.path.splitext(file.filename)[1] if file.filename else ""
        filename = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(file.file.read())
        return f"{tracking_number}/{filename}"

    async def upload(
        self,
        tracking_number: str,
        tax_plate: Optional[UploadFile],
        other: List[UploadFile],
    ) -> DocumentResponseSchema:
        try:
            registiration = self.registiration_repository.get_by_field("tracking_number", tracking_number)
            if not registiration:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail="Başvuru bulunamadı.")

            existing = self.document_repository.get_by_field("registiration_id", registiration.id)

            tax_plate_path = None
            if tax_plate:
                tax_plate_path = self._save_file(tracking_number, tax_plate)

            other_paths = [self._save_file(tracking_number, f) for f in other if f.filename]

            if existing:
                update_data = {}
                if tax_plate_path:
                    update_data["tax_plate"] = tax_plate_path
                if other_paths:
                    current_other = existing.other or []
                    update_data["other"] = current_other + other_paths
                doc = self.document_repository.update(existing, update_data)
            else:
                doc = self.document_repository.create({
                    "registiration_id": registiration.id,
                    "tax_plate": tax_plate_path,
                    "other": other_paths if other_paths else None,
                })

            self.db.commit()
            return DocumentResponseSchema(**doc.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            self.db.rollback()
            raise e

