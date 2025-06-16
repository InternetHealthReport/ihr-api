from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, BigInteger, PrimaryKeyConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP


class DelayAlarms(Base):
    __tablename__ = 'ihr_delay_alarms'


    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __indexes__ = [
        {
            'name': 'ihr_delay_alarms_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        }
    ]

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day'
    }

    id = Column(BigInteger, autoincrement=True)
    timebin = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        doc='Timestamp of reported alarm.'
    )
    ip = Column(
        String(64),
        nullable=False,
    )
    link = Column(
        String(128),
        nullable=False,
        doc='Pair of IP addresses corresponding to the reported link.'
    )
    medianrtt = Column(
        Float,
        nullable=False,
        default=0.0,
        doc='Median differential RTT observed during the alarm.'
    )
    diffmedian = Column(
        Float,
        nullable=False,
        default=0.0,
        doc='Difference between the link usual median RTT and the median RTT observed during the alarm.'
    )
    deviation = Column(
        Float,
        nullable=False,
        default=0.0,
        doc='Distance between observed delays and the past usual values normalized by median absolute deviation.'
    )
    nbprobes = Column(
        Integer,
        nullable=False,
        default=0,
        doc='Number of Atlas probes monitoring this link at the reported time window.'
    )
    msm_prb_ids = Column(
        JSONB,
        nullable=True,
        default=None,
        doc='List of Atlas measurement IDs and probe IDs used to compute this alarm.'
    )
    asn_id = Column(
        BigInteger,
        ForeignKey('ihr_asn.number', ondelete='CASCADE'),
        nullable=False,
        doc='ASN or IXPID of the reported network.'
    )

    asn_relation = relationship('ASN', backref='delay_alarms')

