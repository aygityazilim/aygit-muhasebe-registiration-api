from sqlalchemy.orm import Session
from shared.models import PreRegistirationModel
from shared.repositories.base import BaseRepository

class PreRegistirationRepository(BaseRepository[PreRegistirationModel]):
    def __init__(self, db: Session):
        super().__init__(model=PreRegistirationModel, db=db)