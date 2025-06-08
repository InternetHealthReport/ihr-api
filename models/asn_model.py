from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from config.database import Base

class ASN(Base):
    __tablename__ = 'ihr_asn'

    number = Column(BigInteger, primary_key=True, doc='Autonomous System Number (ASN) or IXP ID. Note that IXP ID are negative to avoid collision.')
    name = Column(String(255), nullable=False, doc='Name registered for the network.')
    tartiflette = Column(Boolean, default=False, nullable=False, doc='True if participate in link delay and forwarding anomaly analysis.')
    disco = Column(Boolean, default=False, nullable=False, doc='True if participate in network disconnection analysis.')
    ashash = Column(Boolean, default=False, nullable=False, doc='True if participate in AS dependency analysis.')

    # Relationship to HegemonyCone
    hegemony_cones = relationship('HegemonyCone', back_populates='asn_relation')


