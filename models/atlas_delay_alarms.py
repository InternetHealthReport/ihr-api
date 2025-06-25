from sqlalchemy import Column, BigInteger, Float, ForeignKey, PrimaryKeyConstraint,Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class AtlasDelayAlarms(Base):
    __tablename__ = 'ihr_atlas_delay_alarms'

    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_atlas_delay_alarms_startpoint_id_timebin_idx',
            'columns': ['startpoint_id', 'timebin DESC'],
        },
        {
            'name': 'ihr_atlas_delay_alarms_endpoint_id_timebin_idx',
            'columns': ['endpoint_id', 'timebin DESC'],
        },
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported alarm.')

    deviation = Column(Float, default=0.0, nullable=False,
                       doc='Significance of the AS Hegemony change.')

    startpoint_id = Column(Integer,
                           ForeignKey('ihr_atlas_location.id', ondelete='CASCADE', name='fk_atlas_delay_startpoint'),
                           nullable=False,
                           doc='Starting location reported as anomalous.')

    endpoint_id = Column(Integer,
                         ForeignKey('ihr_atlas_location.id', ondelete='CASCADE', name='fk_atlas_delay_endpoint'),
                         nullable=False,
                         doc='Ending location reported as anomalous.')

    startpoint = relationship('AtlasLocation', foreign_keys=[startpoint_id], backref='anomalous_startpoint')
    endpoint = relationship('AtlasLocation', foreign_keys=[endpoint_id], backref='anomalous_endpoint')
