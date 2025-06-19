from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class ForwardingAlarmsMsms(Base):
    __tablename__ = 'ihr_forwarding_alarms_msms'

    __indexes__ = [{
        'name': 'ihr_forwarding_alarms_msms_alarm_id',
        'columns': ['alarm_id']
    }]

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    msmid = Column(BigInteger, default=0, nullable=False)

    probeid = Column(Integer, default=0, nullable=False)

    alarm_id = Column(BigInteger, nullable=False)
