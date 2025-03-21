-- First create the flight_status table and insert status values
CREATE TABLE flight_status (
    status VARCHAR(20) PRIMARY KEY
);

INSERT IGNORE INTO flight_status (status) VALUES
    ('SCHEDULED'),
    ('ACTIVE'),
    ('LANDED'),
    ('CANCELLED'),
    ('DIVERTED'),
    ('DELAYED');

-- Create airports table with default values
CREATE TABLE airports (
    iata_code CHAR(3) PRIMARY KEY,
    icao_code CHAR(4) UNIQUE,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) DEFAULT 'Unknown',
    country VARCHAR(50) DEFAULT 'Unknown',
    latitude FLOAT,
    longitude FLOAT,
    timezone VARCHAR(50)
);

-- Create airlines table with nullable fields
CREATE TABLE airlines (
    airline_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) DEFAULT 'Unknown Airline',
    iata_code CHAR(2) UNIQUE,
    icao_code CHAR(3) UNIQUE,
    country VARCHAR(50) DEFAULT 'Unknown',
    active BOOLEAN DEFAULT TRUE
);

-- Create flights table with modified constraints
-- CREATE TABLE flights (
--     flight_id INT AUTO_INCREMENT PRIMARY KEY,
--     flight_number VARCHAR(10) NOT NULL,
--     airline_id INT NOT NULL,
--     departure_airport CHAR(3),
--     arrival_airport CHAR(3),
--     scheduled_departure DATETIME NOT NULL,
--     scheduled_arrival DATETIME,
--     actual_departure DATETIME,
--     actual_arrival DATETIME,
--     estimated_departure DATETIME,
--     estimated_arrival DATETIME,
--     status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
--     delay_minutes INT DEFAULT 0,
--     aircraft_registration VARCHAR(20),
--     aircraft_type VARCHAR(50),
--     FOREIGN KEY (airline_id) REFERENCES airlines(airline_id),
--     FOREIGN KEY (departure_airport) REFERENCES airports(iata_code),
--     FOREIGN KEY (arrival_airport) REFERENCES airports(iata_code),
--     FOREIGN KEY (status) REFERENCES flight_status(status)
-- );

-- Create flight_status_updates table
CREATE TABLE flight_status_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    status_update_time DATETIME DEFAULT NULL,
    actual_departure DATETIME,
    estimated_departure DATETIME,
    delay_minutes INT DEFAULT 0,
    delay_reason VARCHAR(200),
    departure_gate VARCHAR(10),
    departure_terminal VARCHAR(10),
    arrival_gate VARCHAR(10),
    arrival_terminal VARCHAR(10),
    baggage_claim VARCHAR(20),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id) ON DELETE CASCADE,
    FOREIGN KEY (status) REFERENCES flight_status(status)
);

-- Create flight_status_updates table
CREATE TABLE flight_status_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    status_update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    actual_departure DATETIME,
    estimated_departure DATETIME,
    delay_minutes INT DEFAULT 0,
    delay_reason VARCHAR(200),
    departure_gate VARCHAR(10),
    departure_terminal VARCHAR(10),
    arrival_gate VARCHAR(10),
    arrival_terminal VARCHAR(10),
    baggage_claim VARCHAR(20),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id) ON DELETE CASCADE,
    FOREIGN KEY (status) REFERENCES flight_status(status)
);

-- Add indexes for better performance
CREATE INDEX idx_flight_number ON flights(flight_number);
CREATE INDEX idx_departure_time ON flights(scheduled_departure);
CREATE INDEX idx_status ON flights(status);
CREATE INDEX idx_flight_updates ON flight_status_updates(flight_id, status_update_time); 