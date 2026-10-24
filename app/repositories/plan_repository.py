from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.repositories.base import BaseRepository


class PlanRepository(BaseRepository[Plan]):
    def __init__(self, db: Session):
        super().__init__(Plan, db)

    def get_by_name(self, name: str) -> Optional[Plan]:
        return self.db.query(Plan).filter(Plan.name == name).first()

    def get_active_plans(self) -> List[Plan]:
        return self.db.query(Plan).filter(Plan.status == "active").all()
