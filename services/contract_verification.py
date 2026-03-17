from sqlalchemy.orm import Session
from fastapi import HTTPException
from shared.repositories import (
    RegistirationRepository,
    RegistirationHistoryRepository,
    ContractVerificationRepository
)
from shared.schemas import RegistirationResponseSchema
from shared.enums import (
    StatusCodeEnum,
    ErrorMessageEnum,
    RegistirationStatusEnum
)
from shared.utils import NETGSMUtils
import random
from datetime import datetime

class ContractVerificationService:
    def __init__(self, db: Session):
        self.db = db
        self.registiration_repository = RegistirationRepository(db=db)
        self.registiration_history_repository = RegistirationHistoryRepository(db=db)
        self.contract_verification_repository = ContractVerificationRepository(db=db)

    async def send_code(self, registiration_number: str) -> None:
        try:
            registiration = self.registiration_repository.get_by_field("tracking_number", registiration_number)
            contracts = self.contract_verification_repository.get_registiration_contracts(registiration.id)
            code_lines = []
            for contract in contracts:
                if contract.registiration_id != registiration.id:
                    raise HTTPException(status_code=StatusCodeEnum.UNAUTHORIZED.value, detail=ErrorMessageEnum.UNAUTHORIZED.value)
                verification_code = str(random.randint(100000, 999999))
                self.contract_verification_repository.update(contract, {"verification_code": verification_code, "sent_date": datetime.now()})
                self.registiration_history_repository.create({"note": f"{contract.type} Verifikasyonu İstendi", "registiration_id": registiration.id, "status": RegistirationStatusEnum.PENDING.value})
                code_lines.append(f"{contract.type.upper()} dogrulama kodunuz: {verification_code}")
            msg = "\n".join(code_lines)
            NETGSMUtils.send_otp(phone=registiration.phone, message=msg)
            self.db.commit()
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            self.db.rollback()
            raise e
        
    async def verifiy_code(self, registiration_number: str, contract_id: int, code: str) -> None:
        try:
            registiration = self.registiration_repository.get_by_field("tracking_number", registiration_number)
            contract = self.contract_verification_repository.get_by_id(contract_id)
            if contract.registiration_id != registiration.id:
                raise  HTTPException(status_code=StatusCodeEnum.UNAUTHORIZED.value, detail=ErrorMessageEnum.UNAUTHORIZED.value)            
            if contract.verification_code != code:
                raise HTTPException(status_code=StatusCodeEnum.BAD_REQUEST.value, detail=ErrorMessageEnum.INVALID_VERIFICATION_CODE.value)
            self.contract_verification_repository.update(contract, {"verified_code": code, "verification_date": datetime.now()})
            self.registiration_history_repository.create({"note": f"{contract.type} Verifikasyonu Yapıldı", "registiration_id": registiration.id, "status": RegistirationStatusEnum.PENDING.value})
            self.db.commit()    
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            self.db.rollback()
            raise e