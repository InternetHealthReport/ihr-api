from sqlalchemy import Column, BigInteger, Integer, Float, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from config.database import Base


class MetisAtlasSelection(Base):
    __tablename__ = 'ihr_metis_atlas_selection'

    __table_args__ = (
        PrimaryKeyConstraint('id','timebin'),
    )

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '7 day',
    }

    __indexes__ = [
        {
            'name': 'ihr_metis_atlas_selection_metric_rank_timebin_idx',
            'columns': ['metric', 'rank', 'timebin']
        }
    ]

    id = Column(BigInteger, autoincrement=True)

    timebin = Column(TIMESTAMP(timezone=True), nullable=False,
                     doc='Time when the ranking is computed. The ranking uses four weeks of data, hence 2022-03-28T00:00 means the ranking using data from 2022-02-28T00:00 to 2022-03-28T00:00.')

    metric = Column(String(16), nullable=False,
                    doc="Distance metric used to compute diversity, possible values are: 'as_path_length', 'ip_hops', 'rtt'")

    rank = Column(Integer, nullable=False,
                  doc='Selecting all ASes with rank less than or equal to 10 (i.e. rank__lte=10), gives the 10 most diverse ASes in terms of the selected metric.')

    af = Column(Integer, nullable=False,
                doc='Address Family (IP version), values are either 4 or 6.')

    mean = Column(Float, default=0.0, nullable=False,
                  doc='The mean distance value (e.g., AS-path length) we get when using all ASes up to this rank. This decreases with increasing rank, since lower ranks represent closer ASes.')

    asn = Column('asn_id',BigInteger,
                    nullable=False,
                    doc="Atlas probes' Autonomous System Number.")
    
    asn_relation = relationship('ASN',
                            primaryjoin='MetisAtlasSelection.asn == ASN.number',
                            foreign_keys=[asn],
                            backref='metis_selections')

