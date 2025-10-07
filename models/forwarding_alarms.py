from sqlalchemy import Column, BigInteger, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class ForwardingAlarms(Base):
    __tablename__ = 'ihr_forwarding_alarms'

    __table_args__ = (
        PrimaryKeyConstraint('timebin','id'),
    )

    __indexes__ = [
        {
            'name': 'ihr_forwarding_alarms_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        }
    ]

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day'
    }

    id = Column(BigInteger, autoincrement=True)
    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported alarm.')
    ip = Column(String(64), nullable=False,
                doc='Reported IP address, seen an unusually high or low number of times in Atlas traceroutes.')

    correlation = Column(Float, default=0.0, nullable=False,
                         doc='Correlation coefficient between the usual forwarding pattern and the forwarding pattern observed during the alarm. Values range between 0 and -1. Lowest values represent the most anomalous patterns.')
    responsibility = Column(Float, default=0.0, nullable=False,
                            doc='Responsibility score of the reported IP in the forwarding pattern change.')
    pktdiff = Column(Float, default=0.0, nullable=False,
                     doc='The difference between the number of times the reported IP is seen in traceroutes compare to its usual appearance.')
    previoushop = Column(String(64), nullable=False,
                         doc='Last observed IP hop on the usual path.')

    msm_prb_ids = Column(JSONB, nullable=True, default=None,
                         doc='List of Atlas measurement and probe IDs used to compute this alarm.')

    asn_id = Column(BigInteger,
                    nullable=False, doc='ASN or IXPID of the reported network.')
