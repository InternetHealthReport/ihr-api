from sqlalchemy import (
    Column, BigInteger, Float, Integer, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class AtlasDelay(Base):
    __tablename__ = 'ihr_atlas_delay'

    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
        'compress': True,
        'compress_segmentby': 'startpoint_id,endpoint_id',
        'compress_orderby': 'timebin',
        'compress_policy': True,
        'compress_after': '7 days'
    }

    __indexes__ = [
        {
            'name': 'ihr_atlas_delay_endpoint_id_timebin_idx',
            'columns': ['endpoint_id', 'timebin DESC'],
        },
        {
            'name': 'ihr_atlas_delay_startpoint_id_endpoint_id_timebin_idx',
            'columns': ['startpoint_id', 'endpoint_id', 'timebin DESC'],
        },
        {
            'name': 'ihr_atlas_delay_startpoint_id_timebin_idx',
            'columns': ['startpoint_id', 'timebin DESC'],
        },
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value.')

    median = Column(Float, default=0.0, nullable=False,
                    doc='Estimated median RTT. RTT values are directly extracted from traceroute (a.k.a. realrtts) and estimated via differential RTTs.')

    nbtracks = Column(Integer, default=0, nullable=False,
                      doc='Number of RTT samples used to compute median RTT (either real or differential RTT).')

    nbprobes = Column(Integer, default=0, nullable=False,
                      doc='Number of Atlas probes used to compute median RTT.')

    entropy = Column(Float, default=0.0, nullable=False,
                     doc="Entropy of RTT samples with regards to probes' ASN. Values close to zero mean that Atlas probes used for these measures are located in the same AS, values close to one means that probes are equally spread across multiple ASes.")

    hop = Column(Integer, default=0, nullable=False,
                 doc='Median number of AS hops between the start and end locations.')

    nbrealrtts = Column(Integer, default=0, nullable=False,
                        doc='Number of RTT samples directly obtained from traceroutes (as opposed to differential RTTs).')

    startpoint_id = Column(BigInteger,
                           ForeignKey(
                               'ihr_atlas_location.id', ondelete='CASCADE', name='fk_atlas_delay_startpoint'),
                           nullable=False,
                           doc='Starting location for the delay estimation.')

    endpoint_id = Column(BigInteger,
                         ForeignKey(
                             'ihr_atlas_location.id', ondelete='CASCADE', name='fk_atlas_delay_endpoint'),
                         nullable=False,
                         doc='Ending location for the delay estimation.')

    startpoint = relationship('AtlasLocation', foreign_keys=[
                              startpoint_id], backref='location_startpoint')
    endpoint = relationship('AtlasLocation', foreign_keys=[
                            endpoint_id], backref='location_endpoint')
