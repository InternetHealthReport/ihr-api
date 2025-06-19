from sqlalchemy import Column, BigInteger, Integer, String, PrimaryKeyConstraint
from config.database import Base


class TRHegemonyIdentifier(Base):
    __tablename__ = 'ihr_tr_hegemony_identifier'

    id = Column(BigInteger, autoincrement=True, primary_key=True)

    name = Column(String(255), nullable=False,
                  doc='Value of the identifier. The meaning depends on the identifier type: <ul><li>type=AS: ASN</li><li>type=IX: PeeringDB IX ID</li><li>type=MB: IXP member (format: ix_id;asn)</li><li>type=IP: Interface IP of an IXP member</li></ul>')

    type = Column(String(4), nullable=False,
                  doc='Type of the identifier. Possible values are: <ul><li>AS: Autonomous System</li><li>IX: IXP</li><li>MB: IXP member</li><li>IP: IXP member IP</li></ul>')

    af = Column(Integer, nullable=False,
                doc='Address family (IP version), values are either 4 or 6.')
