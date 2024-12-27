from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Neighborhood(Base):
    __tablename__ = "neighborhood"

    neigh_num = Column(Integer, primary_key=True, index=True)
    neigh_name = Column(String(255), nullable=False)
    rank = Column(Integer, nullable=False)

    listings = relationship("Listing", back_populates="neighborhood")