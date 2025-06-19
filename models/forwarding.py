from sqlalchemy import Column, BigInteger, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class Forwarding(Base):
    __tablename__ = 'ihr_forwarding'

    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_forwarding_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC'],
        },
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value.')

    magnitude = Column(Float, default=0.0, nullable=False,
                       doc='Cumulated link delay deviation. Values close to zero represent usual delays for the network, whereas higher values stand for significant links congestion in the monitored network.')

    asn_id = Column(BigInteger,
                    ForeignKey('ihr_asn.number', ondelete='CASCADE', name='fk_forwarding_asn_id'),
                    nullable=False,
                    doc='ASN or IXP ID of the monitored network (see number in /network/).')

    asn = relationship('ASN', foreign_keys=[asn_id])
