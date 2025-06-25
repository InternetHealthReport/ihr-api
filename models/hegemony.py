from sqlalchemy import Column, BigInteger, Float, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class Hegemony(Base):
    __tablename__ = 'ihr_hegemony'

    __table_args__ = (
        PrimaryKeyConstraint('id', 'timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
        'compress': True,
        'compress_segmentby': 'af,originasn_id,asn_id',
        'compress_orderby': 'timebin',
        'compress_policy': True,
        'compress_after': '7 days'
    }

    __indexes__ = [
        {
            'name': 'ihr_hegemony_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC'],
        },
        {
            'name': 'ihr_hegemony_originasn_id_timebin_idx',
            'columns': ['originasn_id', 'timebin DESC'],
        },
        {
            'name': 'ihr_hegemony_asn_id_originasn_id_timebin_idx',
            'columns': ['asn_id', 'originasn_id', 'timebin DESC'],
        },
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value.')

    hege = Column(Float, default=0.0, nullable=False,
                  doc='AS Hegemony is the estimated fraction of paths towards the originasn. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies.')

    af = Column(Integer, default=0, nullable=False,
                doc='Address Family (IP version), values are either 4 or 6.')

    asn_id = Column(BigInteger,
                    nullable=False,
                    doc='Dependency. Transit network commonly seen in BGP paths towards originasn.')

    originasn_id = Column(BigInteger,
                          nullable=False,
                          doc='Dependent network, it can be any public ASN. Retrieve all dependencies of a network by setting only this parameter and a timebin.')

 
   
