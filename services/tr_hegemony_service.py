from sqlalchemy.orm import Session
from repositories.tr_hegemony_repository import TRHegemonyRepository
from dtos.tr_hegemony_dto import TRHegemonyDTO
from typing import Optional, List, Tuple
from datetime import datetime


class TRHegemonyService:
    def __init__(self):
        self.tr_hegemony_repository = TRHegemonyRepository()

    def get_tr_hegemony(
        self,
        db: Session,
        timebin: Optional[datetime] = None,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        origin_names: Optional[str] = None,
        dependency_names: Optional[str] = None,
        origin_type: Optional[str] = None,
        dependency_type: Optional[str] = None,
        origin_af: Optional[int] = None,
        dependency_af: Optional[int] = None,
        hege: Optional[float] = None,
        hege_gte: Optional[float] = None,
        hege_lte: Optional[float] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[TRHegemonyDTO], int]:
        
        hegemony_data, total_count = self.tr_hegemony_repository.get_tr_hegemony(
            db,
            timebin=timebin,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            origin_names=origin_names,
            dependency_names=dependency_names,
            origin_type=origin_type,
            dependency_type=dependency_type,
            origin_af=origin_af,
            dependency_af=dependency_af,
            hege=hege,
            hege_gte=hege_gte,
            hege_lte=hege_lte,
            af=af,
            page=page,
            order_by=order_by
        )

        return [TRHegemonyDTO.from_model(hegemony) for hegemony in hegemony_data], total_count