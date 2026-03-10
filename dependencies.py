from fastapi import Depends
from sqlalchemy.orm import Session
from shared.db import get_db
from services.registiration import RegistirationService

def get_registiration_service(db: Session = Depends(get_db)) -> RegistirationService:
    return RegistirationService(db=db)