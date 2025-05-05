from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BookingCreate, Booking
from app.crud import create_booking, get_bookings, get_booking, delete_booking
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/bookings", tags=["bookings"])  # Убедитесь, что имя переменной "router"

@router.post("/", response_model=Booking)
def create_new_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_booking(db=db, booking=booking, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/", response_model=list[Booking])
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_bookings(db, skip=skip, limit=limit)

@router.delete("/{booking_id}")
def delete_existing_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_booking = get_booking(db, booking_id=booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if db_booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own bookings"
        )
    
    delete_booking(db, booking_id=booking_id)
    return {"message": "Booking deleted successfully"}

# Явно экспортируем роутер
__all__ = ["router"]