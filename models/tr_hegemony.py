from sqlalchemy import Column, BigInteger, Integer, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class TRHegemony(Base):
    __tablename__ = 'ihr_tr_hegemony'

    __table_args__ = (
        PrimaryKeyConstraint('id','timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_tr_hegemony_dependency_id_timebin_idx',
            'columns': ['dependency_id', 'timebin DESC']
        },
        {
            'name': 'ihr_tr_hegemony_origin_id_timebin_idx',
            'columns': ['origin_id', 'timebin DESC']
        }
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Timestamp of reported value. The computation uses four weeks of data, hence 2022-03-28T00:00 means the values are based on data from 2022-02-28T00:00 to 2022-03-28T00:00.')

    hege = Column(Float, default=0.0, nullable=False,
                  doc='AS Hegemony is the estimated fraction of paths towards the origin. The values range between 0 and 1, low values represent a small number of path (low dependency) and values close to 1 represent strong dependencies.')

    af = Column(Integer, default=0, nullable=False,
                doc='Address family (IP version), values are either 4 or 6.')

    nbsamples = Column(Integer, default=0, nullable=False,
                       doc='The number of probe ASes for which we have traceroutes to the origin in the time interval. We only include AS Hegemony values that are based on traceroutes from at least ten probe ASes.')

    dependency_id = Column(BigInteger,
                           ForeignKey('ihr_tr_hegemony_identifier.id', ondelete='CASCADE',
                                      name='fk_tr_hegemony_dependency_id'),
                           nullable=False,
                           doc='Dependency. Transit network or IXP commonly seen in traceroutes towards the origin.')

    origin_id = Column(BigInteger,
                       ForeignKey('ihr_tr_hegemony_identifier.id', ondelete='CASCADE',
                                  name='fk_tr_hegemony_origin_id'),
                       nullable=False,
                       doc='Dependent network, it can be any public ASN. Retrieve all dependencies of a network by setting only this parameter and a timebin.')

    dependency = relationship('TRHegemonyIdentifier', foreign_keys=[dependency_id])
    origin = relationship('TRHegemonyIdentifier', foreign_keys=[origin_id], back_populates='local_graph')
