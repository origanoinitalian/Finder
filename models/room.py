from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Room(Base):
    __tablename__ = "room"

    airbnb_id = Column(Integer, ForeignKey("listings.airbnb_id"), primary_key=True, index=True)
    host_id = Column(Integer, nullable=False)
    room_type = Column(String(255), nullable=False)
    availability = Column(Boolean, nullable=False, default=True)
    check_in = Column(Date, nullable=True)
    check_out = Column(Date, nullable=True)

    # Relationship to Listing
    listing = relationship("Listing", back_populates="room")