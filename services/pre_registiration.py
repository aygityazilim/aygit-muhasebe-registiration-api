from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import (
    PreRegistirationRepository,
    PreRegistirationHistoryRepository
)
from shared.schemas import (
    PreRegistirationResponseSchema,
    PreRegistirationCreateSchema,
    PreRegistirationUpdateSchema
)
from shared.enums import RegistirationStatusEnum
import random

class PreRegistirationService:
    def __init__(self, db: Session):
        self.db = db
        self.pre_registiration_repository = PreRegistirationRepository(db=db)
        self.pre_registiration_history_repository = PreRegistirationHistoryRepository(db=db)

    
    async def create(self, payload: PreRegistirationCreateSchema) -> PreRegistirationResponseSchema:
        try:
            tracking_number = str(random.randint(10**19, 10**20 - 1))
            existing_registiration = self.pre_registiration_repository.get_by_field("tracking_number", tracking_number)
            
            while existing_registiration is not None:
                tracking_number = str(random.randint(10**19, 10**20 - 1))
                existing_registiration = self.pre_registiration_repository.get_by_field("tracking_number", tracking_number)
            
            payload.tracking_number = tracking_number
            payload.status = RegistirationStatusEnum.PENDING.value
            data = self.pre_registiration_repository.create(payload.model_dump(mode="json", exclude_none=True))
            self.pre_registiration_history_repository.create({"note": "Oluşturuldu", "status": RegistirationStatusEnum.PENDING.value, "pre_registiration_id": data.id})            
            data = PreRegistirationResponseSchema(**data.to_dict())
            self.db.commit()
            return data
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            self.db.rollback()
            raise e