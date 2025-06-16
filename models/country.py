from sqlalchemy import Column, String, Boolean,text
from config.database import Base


class Country(Base):
    __tablename__ = "ihr_country"

    code = Column(String(4), primary_key=True)
    name = Column(String(255), nullable=False)
    tartiflette = Column(Boolean, default=False, nullable=False)
    disco = Column(Boolean, default=False, nullable=False)
