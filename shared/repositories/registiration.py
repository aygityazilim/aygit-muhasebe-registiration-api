from sqlalchemy.orm import Session
from shared.models import RegistirationModel
from shared.repositories.base import BaseRepository

class RegistirationRepository(BaseRepository[RegistirationModel]):
    def __init__(self, db: Session):
        super().__init__(model=RegistirationModel, db=db)