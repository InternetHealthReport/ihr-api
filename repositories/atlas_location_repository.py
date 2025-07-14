from sqlalchemy.orm import Session
from models.atlas_location import AtlasLocation
from typing import Optional, List, Tuple
from globals import page_size


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
        query = db.query(AtlasLocation)

        # Apply filters
        if name:
            query = query.filter(AtlasLocation.name.ilike(f"%{name}%"))
        if type:
            query = query.filter(AtlasLocation.type == type)
        if af:
            query = query.filter(AtlasLocation.af == af)

        total_count = query.count()

        # Apply ordering
        if order_by and hasattr(AtlasLocation, order_by):
            query = query.order_by(getattr(AtlasLocation, order_by))
        

        # Apply pagination
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return results, total_count
