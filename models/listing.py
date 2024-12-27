from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Listing(Base):
    __tablename__ = "listings"

    airbnb_id = Column(Integer, primary_key=True, index=True)
    airbnb_name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    host_id = Column(Integer, nullable=False)
    neigh_num = Column(Integer, ForeignKey("neighborhood.neigh_num"), nullable=False)

    neighborhood = relationship("Neighborhood", back_populates="listings")
    room = relationship("Room", back_populates="listing", uselist=False)