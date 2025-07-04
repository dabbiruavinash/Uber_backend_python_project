-- Users and Authentication
CREATE TABLE users (
    user_id VARCHAR2(36) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(15) UNIQUE NOT NULL,
    password_hash VARCHAR2(256) NOT NULL,
    user_type VARCHAR2(10) CHECK (user_type IN ('passenger', 'driver', 'admin')),
    is_active NUMBER(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Vehicles
CREATE TABLE vehicles (
    vehicle_id VARCHAR2(36) PRIMARY KEY,
    registration_number VARCHAR2(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR2(20) CHECK (vehicle_type IN ('mini', 'sedan', 'suv', 'premium', 'auto', 'bike')),
    make VARCHAR2(50) NOT NULL,
    model VARCHAR2(50) NOT NULL,
    year NUMBER(4) NOT NULL,
    color VARCHAR2(30),
    is_active NUMBER(1) DEFAULT 1,
    insurance_number VARCHAR2(50),
    insurance_expiry DATE,
    puc_expiry DATE,
    current_driver_id VARCHAR2(36) REFERENCES users(user_id)
);

-- Driver Details
CREATE TABLE driver_details (
    driver_id VARCHAR2(36) PRIMARY KEY REFERENCES users(user_id),
    license_number VARCHAR2(50) UNIQUE NOT NULL,
    license_expiry DATE NOT NULL,
    total_trips NUMBER DEFAULT 0,
    average_rating NUMBER(3,2) DEFAULT 0,
    is_verified NUMBER(1) DEFAULT 0,
    current_status VARCHAR2(20) CHECK (current_status IN ('offline', 'available', 'in_trip', 'on_break')),
    current_latitude NUMBER(10,6),
    current_longitude NUMBER(10,6),
    wallet_balance NUMBER(10,2) DEFAULT 0
);

-- Driver Documents
CREATE TABLE driver_documents (
    document_id VARCHAR2(36) PRIMARY KEY,
    driver_id VARCHAR2(36) REFERENCES driver_details(driver_id),
    document_type VARCHAR2(20) CHECK (document_type IN ('license', 'rc', 'insurance', 'puc', 'aadhaar', 'pan')),
    document_number VARCHAR2(50),
    document_url VARCHAR2(256),
    verified_on TIMESTAMP,
    verified_by VARCHAR2(36) REFERENCES users(user_id)
);

-- Bookings
CREATE TABLE bookings (
    booking_id VARCHAR2(36) PRIMARY KEY,
    passenger_id VARCHAR2(36) REFERENCES users(user_id),
    driver_id VARCHAR2(36) REFERENCES users(user_id),
    vehicle_id VARCHAR2(36) REFERENCES vehicles(vehicle_id),
    pickup_latitude NUMBER(10,6) NOT NULL,
    pickup_longitude NUMBER(10,6) NOT NULL,
    dropoff_latitude NUMBER(10,6) NOT NULL,
    dropoff_longitude NUMBER(10,6) NOT NULL,
    vehicle_type VARCHAR2(20) NOT NULL,
    status VARCHAR2(20) CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed', 'in_progress')),
    estimated_fare NUMBER(10,2),
    actual_fare NUMBER(10,2),
    distance_km NUMBER(6,2),
    duration_minutes NUMBER(6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP,
    completed_at TIMESTAMP,
    cancellation_reason VARCHAR2(200)
);

-- Trips
CREATE TABLE trips (
    trip_id VARCHAR2(36) PRIMARY KEY,
    booking_id VARCHAR2(36) REFERENCES bookings(booking_id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    start_latitude NUMBER(10,6),
    start_longitude NUMBER(10,6),
    end_latitude NUMBER(10,6),
    end_longitude NUMBER(10,6),
    fare NUMBER(10,2) NOT NULL,
    driver_earnings NUMBER(10,2) NOT NULL,
    uber_commission NUMBER(10,2) NOT NULL,
    surge_multiplier NUMBER(3,2) DEFAULT 1.0,
    payment_id VARCHAR2(50)
);

-- Trip Route Tracking
CREATE TABLE trip_route_points (
    point_id VARCHAR2(36) PRIMARY KEY,
    trip_id VARCHAR2(36) REFERENCES trips(trip_id),
    latitude NUMBER(10,6) NOT NULL,
    longitude NUMBER(10,6) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sequence_number NUMBER NOT NULL
);

-- Payments
CREATE TABLE payments (
    payment_id VARCHAR2(36) PRIMARY KEY,
    booking_id VARCHAR2(36) REFERENCES bookings(booking_id),
    amount NUMBER(10,2) NOT NULL,
    payment_method VARCHAR2(20) CHECK (payment_method IN ('credit_card', 'debit_card', 'upi', 'wallet', 'netbanking')),
    payment_status VARCHAR2(20) CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    transaction_id VARCHAR2(100),
    payment_gateway VARCHAR2(50),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    refund_amount NUMBER(10,2) DEFAULT 0
);

-- Ratings
CREATE TABLE ratings (
    rating_id VARCHAR2(36) PRIMARY KEY,
    trip_id VARCHAR2(36) REFERENCES trips(trip_id),
    rated_entity_id VARCHAR2(36) NOT NULL,
    rater_id VARCHAR2(36) NOT NULL,
    entity_type VARCHAR2(10) CHECK (entity_type IN ('driver', 'passenger', 'vehicle')),
    rating_value NUMBER(1) CHECK (rating_value BETWEEN 1 AND 5),
    comments VARCHAR2(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    notification_id VARCHAR2(36) PRIMARY KEY,
    user_id VARCHAR2(36) REFERENCES users(user_id),
    title VARCHAR2(100) NOT NULL,
    message VARCHAR2(500) NOT NULL,
    notification_type VARCHAR2(20) CHECK (notification_type IN ('booking', 'payment', 'promotion', 'system')),
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

-- Pricing
CREATE TABLE pricing_config (
    config_id VARCHAR2(36) PRIMARY KEY,
    city VARCHAR2(50) NOT NULL,
    vehicle_type VARCHAR2(20) NOT NULL,
    base_fare NUMBER(10,2) NOT NULL,
    per_km_rate NUMBER(10,2) NOT NULL,
    per_minute_rate NUMBER(10,2) NOT NULL,
    min_fare NUMBER(10,2) NOT NULL,
    surge_multiplier_cap NUMBER(3,2) DEFAULT 3.0,
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_until TIMESTAMP,
    is_active NUMBER(1) DEFAULT 1
);

-- Driver Scheduling
CREATE TABLE driver_schedules (
    schedule_id VARCHAR2(36) PRIMARY KEY,
    driver_id VARCHAR2(36) REFERENCES driver_details(driver_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR2(20) CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Indexes for Performance
CREATE INDEX idx_driver_location ON driver_details(current_latitude, current_longitude);
CREATE INDEX idx_booking_status ON bookings(status);
CREATE INDEX idx_trip_booking ON trips(booking_id);
CREATE INDEX idx_payment_booking ON payments(booking_id);
CREATE INDEX idx_vehicle_type ON vehicles(vehicle_type);
CREATE INDEX idx_user_type ON users(user_type);