from sqlalchemy import Column, Integer, Float, ForeignKey, PrimaryKeyConstraint, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class HegemonyAlarms(Base):
    __tablename__ = 'ihr_hegemony_alarms'

    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_hegemony_alarms_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        },
        {
            'name': 'ihr_hegemony_alarms_originasn_id_timebin_idx',
            'columns': ['originasn_id', 'timebin DESC']
        }
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported alarm.')

    deviation = Column(Float, default=0.0, nullable=False,
                       doc='Significance of the AS Hegemony change.')

    af = Column(Integer, nullable=False,
                doc='Address Family (IP version), values are either 4 or 6.')

    asn_id = Column(BigInteger,
                    nullable=False,
                    doc='ASN of the anomalous dependency (transit network).')

    originasn_id = Column(BigInteger,
                          nullable=False,
                          doc='ASN of the reported dependent network.')
