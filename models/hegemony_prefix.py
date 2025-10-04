from sqlalchemy import Column, BigInteger, Integer, Float, String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class HegemonyPrefix(Base):
    __tablename__ = 'ihr_hegemony_prefix'

    __table_args__ = (
        PrimaryKeyConstraint('timebin','id'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_hegemony_prefix_prefix_timebin_idx',
            'columns': ['prefix', 'timebin DESC']
        },
        {
            'name': 'ihr_hegemony_prefix_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        },
        {
            'name': 'ihr_hegemony_prefix_originasn_id_timebin_idx',
            'columns': ['originasn_id', 'timebin DESC']
        },
        {
            'name': 'ihr_hegemony_prefix_country_id_timebin_idx',
            'columns': ['country_id', 'timebin DESC']
        }
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value.')

    prefix = Column(String(64), nullable=False,
                    doc='Monitored prefix (IPv4 or IPv6).')

    hege = Column(Float, default=0.0, nullable=False,
                  doc='AS Hegemony is the estimated fraction of paths towards the monitored prefix. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies.')

    af = Column(Integer, default=0, nullable=False,
                doc='Address Family (IP version), values are either 4 or 6.')

    visibility = Column(Float, default=0.0, nullable=False,
                        doc='Percentage of BGP peers that see this prefix.')

    rpki_status = Column(String(32), nullable=False,
                         doc='Route origin validation state for the monitored prefix and origin AS using RPKI.')

    irr_status = Column(String(32), nullable=False,
                        doc='Route origin validation state for the monitored prefix and origin AS using IRR.')

    delegated_prefix_status = Column(String(32), nullable=False,
                                     doc="Status of the monitored prefix in the RIR's delegated stats. Status other than 'assigned' are usually considered as bogons.")

    delegated_asn_status = Column(String(32), nullable=False,
                                  doc="Status of the origin ASN in the RIR's delegated stats. Status other than 'assigned' are usually considered as bogons.")

    descr = Column(String(64), nullable=False,
                   doc='Prefix description from IRR (maximum 64 characters).')

    moas = Column(Boolean, default=False, nullable=False,
                  doc='True if the prefix is originated by multiple ASNs.')

    asn = Column('asn_id', BigInteger,
                 nullable=False,
                 doc='Dependency. Network commonly seen in BGP paths towards monitored prefix.')

    originasn = Column('originasn_id', BigInteger,
                       nullable=False,
                       doc='Network seen as originating the monitored prefix.')

    country = Column('country_id', String(4),
                     nullable=False,
                     doc="Country for the monitored prefix identified by Maxmind's Geolite2 geolocation database.")

    asn_relation = relationship('ASN',
                                primaryjoin='HegemonyPrefix.asn == ASN.number',
                                foreign_keys=[asn])

    originasn_relation = relationship('ASN',
                                      primaryjoin='HegemonyPrefix.originasn == ASN.number',
                                      foreign_keys=[originasn])
    
    country_relation = relationship('Country',
                                      primaryjoin='HegemonyPrefix.country == Country.code',
                                      foreign_keys=[country])
