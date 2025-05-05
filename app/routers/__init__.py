from .auth import router as auth_router
from .resources import router as resources_router
from .bookings import router as bookings_router

__all__ = ["auth_router", "resources_router", "bookings_router"]