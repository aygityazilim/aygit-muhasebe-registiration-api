from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import (
    RegistirationRepository,
    ContractVerificationRepository,
    RegistirationHistoryRepository,
    DocumentRepository
)
from shared.schemas import (
    RegistirationResponseSchema,
    RegistirationCreateSchema,
    ContractVerificationResponseSchema,
    DocumentResponseSchema
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
        self.document_repository = DocumentRepository(db=db)
    
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

            contracts_data = []

            for contract in contracts:
                created_contract = self.contract_verification_repository.create(contract)
                contracts_data.append(ContractVerificationResponseSchema(**created_contract.to_dict()))

            data = data.to_dict()
            data["contracts"] = contracts_data
            data["document"] = None
            data = RegistirationResponseSchema(**data)
            
            self.db.commit()
            return data
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            self.db.rollback()
            raise e
        
    async def get_one(self, number: str) -> RegistirationResponseSchema:
        registiration = self.registiration_repository.get_by_field("tracking_number", number)
        contracts = self.contract_verification_repository.get_registiration_contracts(registiration.id)
        document = self.document_repository.get_by_field("registiration_id", registiration.id)

        data = registiration.to_dict()
        data["contracts"] = [ContractVerificationResponseSchema(**contract.to_dict()) for contract in contracts]
        data["document"] = DocumentResponseSchema(**document.to_dict()) if document else None

        return data
