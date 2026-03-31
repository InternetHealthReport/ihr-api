from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.atlas_location import AtlasLocation
from typing import Optional, List, Tuple
from utils import page_size


class AtlasLocationRepository:
    def get_all(
        self,
        db: Session,
        name: Optional[str] = None,
        type: Optional[str] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[AtlasLocation], int]:
        stmt = select(AtlasLocation)

        if name:
            stmt = stmt.where(AtlasLocation.name.ilike(f"%{name}%"))
        if type:
            stmt = stmt.where(AtlasLocation.type == type)
        if af:
            stmt = stmt.where(AtlasLocation.af == af)

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(AtlasLocation, order_by):
            stmt = stmt.order_by(getattr(AtlasLocation, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).all()

        return results, total_count
