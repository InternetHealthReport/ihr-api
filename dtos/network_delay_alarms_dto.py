from pydantic import BaseModel
from datetime import datetime


class NetworkDelayAlarmsDTO(BaseModel):
    timebin: datetime
    startpoint_type: str
    startpoint_name: str
    startpoint_af: int
    endpoint_type: str
    endpoint_name: str
    endpoint_af: int
    deviation: float

    class Config:
        from_attributes = True

    @staticmethod
    def from_model(atlas_delay_alarm):
        return NetworkDelayAlarmsDTO(
            timebin=atlas_delay_alarm.timebin,
            startpoint_type=atlas_delay_alarm.startpoint_relation.type,
            startpoint_name=atlas_delay_alarm.startpoint_relation.name,
            startpoint_af=atlas_delay_alarm.startpoint_relation.af,
            endpoint_type=atlas_delay_alarm.endpoint_relation.type,
            endpoint_name=atlas_delay_alarm.endpoint_relation.name,
            endpoint_af=atlas_delay_alarm.endpoint_relation.af,
            deviation=atlas_delay_alarm.deviation
        )
