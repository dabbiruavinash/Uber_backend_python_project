# API Layer Integration
# Update the API endpoints to use Oracle database:

from fastapi import APIRouter, Depends, HTTPException
from domain.user.service import UserService
from domain.booking.service import BookingService
from core.database import db

router = APIRouter()
user_service = UserService()
booking_service = BookingService()

@router.post("/bookings", response_model=BookingResponse)
async def create_booking(booking_request: BookingRequest, user: dict = Depends(get_current_user)):
    try:
        with db.get_connection() as conn:
            # Find nearby drivers
            drivers = user_service.get_nearby_drivers(
                booking_request.pickup_lat,
                booking_request.pickup_lng
            )
            
            if not drivers:
                raise HTTPException(status_code=404, detail="No drivers available")
                
            # Create booking
            booking_id = booking_service.create_booking(
                user["user_id"],
                drivers[0]["user_id"],
                booking_request.pickup_lat,
                booking_request.pickup_lng,
                booking_request.dropoff_lat,
                booking_request.dropoff_lng,
                booking_request.vehicle_type
            )
            
            return {
                "booking_id": booking_id,
                "status": "confirmed",
                "driver_details": drivers[0],
                "estimated_fare": 250.0  # Would calculate properly
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))