from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, BigInteger,PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class HegemonyCountry(Base):
    __tablename__ = 'ihr_hegemony_country'

    __table_args__ = (
        PrimaryKeyConstraint('id','timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_hegemony_country_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        },
        {
            'name': 'ihr_hegemony_country_country_id_timebin_idx',
            'columns': ['country_id', 'timebin DESC']
        }
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value.')

    hege = Column(Float, default=0.0, nullable=False,
                  doc='AS Hegemony is the estimated fraction of paths towards the monitored country. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies.')

    af = Column(Integer, default=0, nullable=False,
                doc='Address Family (IP version), values are either 4 or 6.')

    weight = Column(Float, default=0.0, nullable=False,
                    doc='Absolute weight given to the ASN for the AS Hegemony calculation.')

    weightscheme = Column(String(16), default='None', nullable=False,
                          doc='Weighting scheme used for the AS Hegemony calculation.')

    transitonly = Column(Boolean, default=False, nullable=False,
                         doc='If True, then origin ASNs of BGP path are ignored (focus only on transit networks).')

    asn_id = Column(BigInteger,
                    ForeignKey('ihr_asn.number', ondelete='CASCADE', name='fk_hegemony_country_asn_id'),
                    nullable=False,
                    doc='Dependency. Network commonly seen in BGP paths towards monitored country.')

    country_id = Column(String(4),
                        ForeignKey('ihr_country.code', ondelete='CASCADE', name='fk_hegemony_country_country_id'),
                        nullable=False,
                        doc='Monitored country. Retrieve all dependencies of a country by setting only this parameter and a timebin.')

    asn = relationship('ASN')
    country = relationship('Country')
