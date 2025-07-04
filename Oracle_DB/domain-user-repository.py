# User Repository

from typing import Optional, Dict, List
from core.repository import OracleRepository
from core.database import db

class UserRepository(OracleRepository):
    def __init__(self):
        super().__init__("users")

    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE user_id = :1"
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    def create(self, user_data: Dict[str, Any]) -> str:
        query = """
        INSERT INTO users (user_id, name, email, phone, password_hash, user_type, is_active)
        VALUES (user_id_seq.NEXTVAL, :1, :2, :3, :4, :5, :6)
        RETURNING user_id INTO :7
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            out_var = cursor.var(cx_Oracle.STRING)
            cursor.execute(query, (
                user_data["name"],
                user_data["email"],
                user_data["phone"],
                user_data["password_hash"],
                user_data["user_type"],
                user_data.get("is_active", 1),
                out_var
            ))
            conn.commit()
            return out_var.getvalue()[0]

    def update(self, user_id: str, updates: Dict[str, Any]) -> bool:
        set_clause = ", ".join(f"{k} = :{i+1}" for i, k in enumerate(updates.keys()))
        values = list(updates.values())
        values.append(user_id)
        
        query = f"UPDATE users SET {set_clause} WHERE user_id = :{len(updates)+1}"
        return self._execute_operation(query, tuple(values))

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE email = :1"
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    def get_drivers_near_location(self, latitude: float, longitude: float, radius_km: float = 5.0) -> List[Dict[str, Any]]:
        query = """
        SELECT u.user_id, u.name, u.phone, v.vehicle_type, 
               d.current_latitude, d.current_longitude,
               SQRT(POWER(69.1 * (d.current_latitude - :lat), 2) + 
               POWER(69.1 * (:lon - d.current_longitude) * COS(d.current_latitude / 57.3), 2)) AS distance_km
        FROM users u
        JOIN driver_details d ON u.user_id = d.driver_id
        LEFT JOIN vehicles v ON d.driver_id = v.current_driver_id
        WHERE u.user_type = 'driver' 
        AND d.current_status = 'available'
        AND u.is_active = 1
        AND SQRT(POWER(69.1 * (d.current_latitude - :lat), 2) + 
            POWER(69.1 * (:lon - d.current_longitude) * COS(d.current_latitude / 57.3), 2)) <= :radius
        ORDER BY distance_km
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (latitude, longitude, latitude, longitude, radius_km))
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]