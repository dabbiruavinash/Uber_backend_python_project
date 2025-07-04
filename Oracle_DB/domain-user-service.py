# Service Layer Integration

from typing import Optional, Dict, List
from domain.user.repository import UserRepository
from core.exceptions import NotFoundError, ValidationError
import hashlib
import secrets

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, user_data: Dict[str, Any]) -> str:
        # Validate input
        if not all(k in user_data for k in ["name", "email", "phone", "password", "user_type"]):
            raise ValidationError("Missing required fields")
        
        # Hash password
        salt = secrets.token_hex(16)
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            user_data["password"].encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        # Store in database
        user_id = self.repository.create({
            "name": user_data["name"],
            "email": user_data["email"],
            "phone": user_data["phone"],
            "password_hash": f"{salt}${hashed_password}",
            "user_type": user_data["user_type"]
        })
        
        return user_id

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.repository.get_by_email(email)
        if not user:
            return None
            
        salt, stored_hash = user["password_hash"].split('$')
        input_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        if input_hash == stored_hash:
            return {k: v for k, v in user.items() if k != "password_hash"}
        return None

    def get_nearby_drivers(self, latitude: float, longitude: float, radius_km: float = 5.0) -> List[Dict[str, Any]]:
        return self.repository.get_drivers_near_location(latitude, longitude, radius_km)

    def update_driver_location(self, driver_id: str, latitude: float, longitude: float) -> bool:
        # First verify this is a driver
        user = self.repository.get_by_id(driver_id)
        if not user or user["user_type"] != "driver":
            raise NotFoundError("Driver not found")
            
        # Update location in driver_details table
        query = """
        UPDATE driver_details 
        SET current_latitude = :1, current_longitude = :2 
        WHERE driver_id = :3
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (latitude, longitude, driver_id))
            conn.commit()
            return cursor.rowcount > 0