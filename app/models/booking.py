from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

#from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint, Boolean  # Добавьте Boolean

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    resource_id = Column(Integer, ForeignKey("resources.id", ondelete="CASCADE"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="bookings")
    resource = relationship("Resource", back_populates="bookings")

    __table_args__ = (
        CheckConstraint('end_time > start_time', name='check_end_time_after_start_time'),
    )