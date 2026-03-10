from fastapi import Depends
from sqlalchemy.orm import Session
from shared.db import get_db
from services.registiration import RegistirationService
from services.contract_verification import ContractVerificationService
from services.document import DocumentService

def get_registiration_service(db: Session = Depends(get_db)) -> RegistirationService:
    return RegistirationService(db=db)

def get_contract_verification_service(db: Session = Depends(get_db)) -> ContractVerificationService:
    return ContractVerificationService(db=db)

def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db=db)