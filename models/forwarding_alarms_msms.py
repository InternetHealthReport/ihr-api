from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class ForwardingAlarmsMsms(Base):
    __tablename__ = 'ihr_forwarding_alarms_msms'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    msmid = Column(BigInteger, default=0, nullable=False)

    probeid = Column(Integer, default=0, nullable=False)

    alarm_id = Column(BigInteger,
                      ForeignKey('ihr_forwarding_alarms.id', ondelete='CASCADE'),
                      nullable=False)

    alarm = relationship('ForwardingAlarms', back_populates='msms')