-- Active Drivers View
CREATE OR REPLACE VIEW active_drivers_view AS
SELECT u.user_id, u.name, u.phone, v.vehicle_type, v.registration_number,
       d.current_latitude, d.current_longitude, d.average_rating
FROM users u
JOIN driver_details d ON u.user_id = d.driver_id
LEFT JOIN vehicles v ON d.driver_id = v.current_driver_id
WHERE u.user_type = 'driver' AND d.current_status = 'available' AND u.is_active = 1;

-- Booking History View
CREATE OR REPLACE VIEW booking_history_view AS
SELECT b.booking_id, b.passenger_id, u1.name AS passenger_name,
       b.driver_id, u2.name AS driver_name, b.vehicle_id,
       b.status, b.estimated_fare, b.actual_fare,
       b.created_at, b.completed_at
FROM bookings b
JOIN users u1 ON b.passenger_id = u1.user_id
LEFT JOIN users u2 ON b.driver_id = u2.user_id;

-- Driver Earnings View
CREATE OR REPLACE VIEW driver_earnings_view AS
SELECT d.driver_id, u.name, COUNT(t.trip_id) AS total_trips,
       SUM(t.driver_earnings) AS total_earnings,
       AVG(r.rating_value) AS avg_rating
FROM driver_details d
JOIN users u ON d.driver_id = u.user_id
LEFT JOIN trips t ON d.driver_id = t.booking_id
LEFT JOIN ratings r ON t.trip_id = r.trip_id AND r.entity_type = 'driver'
GROUP BY d.driver_id, u.name;