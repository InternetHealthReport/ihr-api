from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, String
from models.asn import ASN
from typing import Optional, List, Tuple
from utils import page_size


class NetworksRepository:
    def get_all(
        self,
        db: Session,
        name: Optional[str] = None,
        numbers: Optional[List[int]] = None,
        number_gte: Optional[int] = None,
        number_lte: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[ASN], int]:
        stmt = select(ASN)

        if name:
            stmt = stmt.where(ASN.name.ilike(f"%{name}%"))
        if numbers:
            stmt = stmt.where(ASN.number.in_(numbers))
        if number_gte:
            stmt = stmt.where(ASN.number >= number_gte)
        if number_lte:
            stmt = stmt.where(ASN.number <= number_lte)
        if search:
            search_value = search
            if search.upper().startswith(("AS", "IX")):
                try:
                    search_value = str(int(search[2:]))
                except ValueError:
                    pass
            stmt = stmt.where(or_(
                ASN.number.cast(String).contains(search_value),
                ASN.name.ilike(f"%{search}%")
            ))

        total_count = db.scalar(select(func.count()).select_from(stmt.subquery()))

        if order_by and hasattr(ASN, order_by):
            stmt = stmt.order_by(getattr(ASN, order_by))

        offset = (page - 1) * page_size
        results = db.scalars(stmt.offset(offset).limit(page_size)).all()

        return results, total_count
