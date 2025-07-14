from pydantic import BaseModel
from datetime import datetime


class TRHegemonyDTO(BaseModel):
    timebin: datetime
    origin_type: str
    origin_name: str
    origin_af: int
    dependency_type: str
    dependency_name: str
    dependency_af: int
    hege: float
    af: int
    nbsamples: int

    class Config:
        from_attributes = True

    @staticmethod
    def from_model(tr_hegemony):
        return TRHegemonyDTO(
            timebin=tr_hegemony.timebin,
            origin_type=tr_hegemony.origin_relation.type,
            origin_name=tr_hegemony.origin_relation.name,
            origin_af=tr_hegemony.origin_relation.af,
            dependency_type=tr_hegemony.dependency_relation.type,
            dependency_name=tr_hegemony.dependency_relation.name,
            dependency_af=tr_hegemony.dependency_relation.af,
            hege=tr_hegemony.hege,
            af=tr_hegemony.af,
            nbsamples=tr_hegemony.nbsamples
        )