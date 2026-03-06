from fastapi import Depends
from sqlalchemy.orm import Session
from shared.db import get_db
from services.pre_registiration import PreRegistirationService

def get_pre_registiration_service(db: Session = Depends(get_db)) -> PreRegistirationService:
    return PreRegistirationService(db=db)