from sqlalchemy import Column, Integer, String, BigInteger
from config.database import Base


class AtlasLocation(Base):
    __tablename__ = 'ihr_atlas_location'
    __indexes__ = [
        {
            'name': 'ihr_atlas_location_af_name_type_idx',
            'columns': ['af','type'],
        },]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        String(255),
        nullable=False,
        doc=(
            "Location identifier. The meaning of values dependend on the location type: "
            "<ul><li>type=AS: ASN</li><li>type=CT: city name, region name, country code</li>"
            "<li>type=PB: Atlas Probe ID</li><li>type=IP: IP version (4 or 6)</li></ul> "
        )
    )
    type = Column(
        String(4),
        nullable=False,
        doc=(
            "Type of location. Possible values are: "
            "<ul><li>AS: Autonomous System</li><li>CT: City</li><li>PB: Atlas Probe</li>"
            "<li>IP: Whole IP space</li></ul>"
        )
    )
    af = Column(
        Integer,
        nullable=False,
        doc="Address Family (IP version), values are either 4 or 6."
    )
