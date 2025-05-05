from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    capacity = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    
    bookings = relationship("Booking", back_populates="resource", cascade="all, delete-orphan")