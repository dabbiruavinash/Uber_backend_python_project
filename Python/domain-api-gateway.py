# API Gateway

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class BookingRequest(BaseModel):
    passenger_id: str
    pickup_location: dict
    dropoff_location: dict
    vehicle_type: str

@app.post("/book")
async def create_booking(booking_request: BookingRequest):
    try:
        # Validate input
        if not booking_request.pickup_location or not booking_request.dropoff_location:
            raise HTTPException(status_code=400, detail="Invalid locations")
        
        # Create booking (would integrate with booking service)
        booking_id = f"book_{datetime.now().timestamp()}"
        booking_response = {
            "booking_id": booking_id,
            "status": "pending",
            "estimated_arrival": "5 minutes",
            "estimated_fare": 150.0  # Would come from pricing service
        }
        
        return booking_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drivers/nearby")
async def get_nearby_drivers(latitude: float, longitude: float, radius: float = 5.0):
    try:
        # Would integrate with location and driver services
        mock_drivers = [
            {
                "driver_id": "driver_1",
                "name": "Rajesh",
                "distance": 1.2,
                "vehicle_type": "mini",
                "rating": 4.8
            },
            {
                "driver_id": "driver_2",
                "name": "Vikram",
                "distance": 2.5,
                "vehicle_type": "sedan",
                "rating": 4.9
            }
        ]
        
        return {"drivers": mock_drivers}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))