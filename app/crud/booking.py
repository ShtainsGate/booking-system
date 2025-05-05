from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List

# Импорты из вашего проекта
from app.models import Booking, Resource  # Модели из models/
from app.schemas import BookingCreate     # Схемы из schemas/

def create_booking(db: Session, booking: BookingCreate, user_id: int) -> Booking:
    # Проверка доступности ресурса
    resource = db.query(Resource).filter(
        Resource.id == booking.resource_id,
        Resource.is_available == True
    ).first()
    
    if not resource:
        raise ValueError("Resource not available")

    # Проверка пересечения бронирований
    overlapping = db.query(Booking).filter(
        Booking.resource_id == booking.resource_id,
        Booking.end_time > booking.start_time,
        Booking.start_time < booking.end_time
    ).first()
    
    if overlapping:
        raise ValueError("Time slot already booked")

    # Создание бронирования
    db_booking = Booking(
        user_id=user_id,
        resource_id=booking.resource_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        #is_active=True
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Остальные функции остаются без изменений
def get_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).offset(skip).limit(limit).all()

def get_booking(db: Session, booking_id: int) -> Booking:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def delete_booking(db: Session, booking_id: int) -> bool:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
        return True
    return False

def get_user_bookings(db: Session, user_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_resource_bookings(db: Session, resource_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.resource_id == resource_id).all()