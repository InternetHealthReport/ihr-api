from sqlalchemy import Column, BigInteger, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from config.database import Base


class DelayAlarmsMsms(Base):
    __tablename__ = 'ihr_delay_alarms_msms'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    msmid = Column(BigInteger, default=0, nullable=False)

    probeid = Column(Integer, default=0, nullable=False)

    alarm_id = Column(BigInteger,
                      ForeignKey('ihr_delay_alarms.id', ondelete='CASCADE',
                                 name='fk_delay_alarms_msms_alarm_id'),
                      nullable=False)

    alarm = relationship('DelayAlarms', foreign_keys=[
                         alarm_id], backref='msmid_entries')
