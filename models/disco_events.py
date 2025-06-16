from sqlalchemy import (
    Column, Integer, String, Float, Boolean, BigInteger
)
from config.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP


class DiscoEvents(Base):
    __tablename__ = 'ihr_disco_events'

    __indexes__ = [{
        'name': 'ihr_disco_events_mongoid_3a488192',
        'columns': ['mongoid']
    }, {
        'name': 'ihr_disco_events_streamtype_streamname_st_bda16df6_idx',
        'columns': ['streamtype', 'streamname', 'starttime', 'endtime']
    }]


    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mongoid = Column(
        String(24),
        nullable=False,
        default='000000000000000000000000',
    )
    streamtype = Column(
        String(10),
        nullable=False,
        doc=(
            "Granularity of the detected event. The possible values are asn, country, admin1, and admin2. "
            "Admin1 represents a wider area than admin2, the exact definition might change from one country to another. "
            "For example 'California, US' is an admin1 stream and 'San Francisco County, California, US' is an admin2 stream."
        )
    )
    streamname = Column(
        String(128),
        nullable=False,
        doc='Name of the topological (ASN) or geographical area where the network disconnection happened.'
    )
    starttime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        doc='Estimated start time of the network disconnection.'
    )
    endtime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        doc=(
            'Estimated end time of the network disconnection. '
            'Equal to starttime if the end of the event is unknown.'
        )
    )
    avglevel = Column(
        Float,
        nullable=False,
        default=0.0,
        doc=(
            'Score representing the coordination of disconnected probes. '
            'Higher values stand for a large number of Atlas probes that disconnected in a very short time frame. '
            'Events with an avglevel lower than 10 are likely to be false positives detection.'
        )
    )
    nbdiscoprobes = Column(
        Integer,
        nullable=False,
        default=0,
        doc='Number of Atlas probes that disconnected around the reported start time.'
    )
    totalprobes = Column(
        Integer,
        nullable=False,
        default=0,
        doc='Total number of Atlas probes active in the reported stream (ASN, Country, or geographical area).'
    )
    ongoing = Column(
        Boolean,
        nullable=False,
        default=False,
        doc='Deprecated, this value is unused'
    )

   
