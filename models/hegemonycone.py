from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP


class HegemonyCone(Base):
    __tablename__ = 'ihr_hegemonycone'

    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __indexes__ = [
        {
            'name': 'ihr_hegemonycone_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        },
    ]

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
        'compress': True,
        'compress_segmentby': 'asn_id,af',
        'compress_orderby': 'timebin',
        'compress_policy': True,
        'compress_after': '7 days'
    }

    id = Column(BigInteger, autoincrement=True)
    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp with time zone.')

    conesize = Column(Integer, default=0, nullable=False,
                      doc="Number of dependent networks, namely, networks that are reached through the asn.")
    af = Column(Integer, default=0, nullable=False,
                doc='Address Family (IP version), values are either 4 or 6.')
    asn_id = Column(BigInteger, ForeignKey('ihr_asn.number', ondelete='CASCADE', name='fk_ihr_hegemonycone_asn_id'),
                    nullable=False, doc='Autonomous System Number (ASN).')

    asn_relation = relationship('ASN', back_populates='hegemony_cones')
