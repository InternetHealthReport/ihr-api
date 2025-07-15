from sqlalchemy.orm import Session
from repositories.metis_atlas_deployment_repository import MetisAtlasDeploymentRepository
from repositories.metis_atlas_selection_repository import MetisAtlasSelectionRepository
from dtos.metis_atlas_deployment_dto import MetisAtlasDeploymentDTO
from dtos.metis_atlas_selection_dto import MetisAtlasSelectionDTO
from typing import Optional, List, Tuple
from datetime import datetime


class MetisService:
    def __init__(self):
        self.metis_atlas_deployment_repository = MetisAtlasDeploymentRepository()
        self.metis_atlas_selection_repository = MetisAtlasSelectionRepository()

    def get_metis_atlas_deployments(
        self,
        db: Session,
        timebin: Optional[datetime] = None,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        rank: Optional[int] = None,
        rank_lte: Optional[int] = None,
        rank_gte: Optional[int] = None,
        metric: Optional[str] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[MetisAtlasDeploymentDTO], int]:
        """
        Get Metis Atlas deployment data with filtering.
        """
        deployments, total_count = self.metis_atlas_deployment_repository.get_all(
            db,
            timebin=timebin,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            rank=rank,
            rank_lte=rank_lte,
            rank_gte=rank_gte,
            metric=metric,
            af=af,
            page=page,
            order_by=order_by
        )

        return [MetisAtlasDeploymentDTO(
            timebin=deployment.timebin,
            metric=deployment.metric,
            rank=deployment.rank,
            asn=deployment.asn,
            af=deployment.af,
            nbsamples=deployment.nbsamples,
            asn_name=deployment.asn_relation.name if deployment.asn_relation else None
        ) for deployment in deployments], total_count

    def get_metis_atlas_selections(
        self,
        db: Session,
        timebin: Optional[datetime] = None,
        timebin_gte: Optional[datetime] = None,
        timebin_lte: Optional[datetime] = None,
        rank: Optional[int] = None,
        rank_lte: Optional[int] = None,
        rank_gte: Optional[int] = None,
        metric: Optional[str] = None,
        af: Optional[int] = None,
        page: int = 1,
        order_by: Optional[str] = None
    ) -> Tuple[List[MetisAtlasSelectionDTO], int]:
        """
        Get Metis Atlas selection data with filtering.
        """
        selections, total_count = self.metis_atlas_selection_repository.get_all(
            db,
            timebin=timebin,
            timebin_gte=timebin_gte,
            timebin_lte=timebin_lte,
            rank=rank,
            rank_lte=rank_lte,
            rank_gte=rank_gte,
            metric=metric,
            af=af,
            page=page,
            order_by=order_by
        )

        return [MetisAtlasSelectionDTO(
            timebin=selection.timebin,
            metric=selection.metric,
            rank=selection.rank,
            asn=selection.asn,
            af=selection.af,
            asn_name=selection.asn_relation.name if selection.asn_relation else None
        ) for selection in selections], total_count
