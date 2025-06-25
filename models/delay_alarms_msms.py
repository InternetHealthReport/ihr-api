from sqlalchemy import Column, BigInteger, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from config.database import Base


class DelayAlarmsMsms(Base):
    __tablename__ = 'ihr_delay_alarms_msms'

    __indexes__=[{
        'name':'ihr_delay_alarms_msms_alarm_id',
        'columns':['alarm_id']
    }]

    id = Column(Integer, primary_key=True, autoincrement=True)

    msmid = Column(BigInteger, default=0, nullable=False)

    probeid = Column(Integer, default=0, nullable=False)

    alarm_id = Column(Integer, nullable=False)
