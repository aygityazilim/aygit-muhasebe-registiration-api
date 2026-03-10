from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import (
    RegistirationRepository,
    ContractVerificationRepository,
    RegistirationHistoryRepository
)
from shared.schemas import (
    RegistirationResponseSchema,
    RegistirationCreateSchema
)
from shared.enums import (
    RegistirationStatusEnum,
    ContractVerificationTypeEnum
)
import random

class RegistirationService:
    def __init__(self, db: Session):
        self.db = db
        self.registiration_repository = RegistirationRepository(db=db)
        self.registiration_history_repository = RegistirationHistoryRepository(db=db)
        self.contract_verification_repository = ContractVerificationRepository(db=db)
    
    async def create(self, payload: RegistirationCreateSchema) -> RegistirationResponseSchema:
        try:
            tracking_number = str(random.randint(10**19, 10**20 - 1))
            existing_registiration = self.registiration_repository.get_by_field("tracking_number", tracking_number)
            
            while existing_registiration is not None:
                tracking_number = str(random.randint(10**19, 10**20 - 1))
                existing_registiration = self.registiration_repository.get_by_field("tracking_number", tracking_number)
            
            payload.tracking_number = tracking_number
            payload.status = RegistirationStatusEnum.PENDING.value
            data = self.registiration_repository.create(payload.model_dump(mode="json", exclude_none=True))
            self.registiration_history_repository.create({"note": "Oluşturuldu", "status": RegistirationStatusEnum.PENDING.value, "registiration_id": data.id})
            contracts = [
                {                                          
                    "link": "https://www.asmadanmuze.com/docs/etk-onay-metni.pdf",        
                    "type": ContractVerificationTypeEnum.ETK.value,
                    "registiration_id": data.id
                },
                {
                    "link": "https://www.sabancivakfi.org/i/assets/documents/Sabanci-Vakfi-KVKK-Aydinlatma-Metni-Tur.pdf",
                    "type": ContractVerificationTypeEnum.KVKK.value,
                    "registiration_id": data.id
                }                
            ]

            for contract in contracts:
                self.contract_verification_repository.create(contract)

            data = RegistirationResponseSchema(**data.to_dict())
            self.db.commit()
            return data
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            self.db.rollback()
            raise e