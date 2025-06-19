from sqlalchemy import Column, BigInteger, Float, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class DiscoProbes(Base):
    __tablename__ = 'ihr_disco_probes'

    __indexes__ = [{
        'name': 'ihr_disco_probes_event_id',
        'columns': ['event_id']
    }]

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    probe_id = Column(Integer, nullable=False,
                      doc='Atlas probe ID of disconnected probe.')

    starttime = Column(TIMESTAMP(timezone=True), nullable=False,
                       doc='Probe disconnection time.')

    endtime = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Reconnection time of the probe, this may not be reported if other probes have reconnected earlier.')

    level = Column(Float, default=0.0, nullable=False,
                   doc='Disconnection level when the probe disconnected.')

    ipv4 = Column(String(64), default='None', nullable=False,
                  doc='Public IP address of the Atlas probe.')

    prefixv4 = Column(String(70), default='None', nullable=False,
                      doc='IP prefix corresponding to the probe.')

    lat = Column(Float, default=0.0, nullable=False,
                 doc='Latitude of the probe during the network detection as reported by RIPE Atlas.')

    lon = Column(Float, default=0.0, nullable=False,
                 doc='Longitude of the probe during the network detection as reported by RIPE Atlas.')

    event_id = Column(BigInteger,
                      ForeignKey('ihr_disco_events.id', ondelete='CASCADE',
                                 name='fk_disco_probes_event_id'),
                      nullable=False,
                      doc='ID of the network disconnection event where this probe is reported.')

    event = relationship('DiscoEvents', foreign_keys=[
                         event_id], backref='discoprobes')
