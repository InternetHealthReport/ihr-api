from sqlalchemy import Column, BigInteger, Float, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class Delay(Base):
    __tablename__ = 'ihr_delay'

    __table_args__ = (
        PrimaryKeyConstraint('timebin','id'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_delay_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC'],
        },
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value.')

    magnitude = Column(Float, default=0.0, nullable=False,
                       doc='Cumulated link delay deviation. Values close to zero represent usual delays for the network, whereas higher values stand for significant links congestion in the monitored network.')

    asn = Column('asn_id', BigInteger, nullable=False,
                 doc='ASN or IXP ID of the monitored network (see number in /network/).')

    # Add relationship without foreign key constraint
    asn_relation = relationship('ASN',
                                primaryjoin='Delay.asn == ASN.number',
                                foreign_keys=[asn],
                                backref='delays')
