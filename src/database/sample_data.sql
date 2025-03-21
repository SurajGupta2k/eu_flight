-- Insert sample data for airports
INSERT IGNORE INTO airports (iata_code, icao_code, name, city, country, latitude, longitude, timezone) VALUES 
    ('FRA', 'EDDF', 'Frankfurt Airport', 'Frankfurt', 'Germany', 50.0379, 8.5622, 'Europe/Berlin'),
    ('MUC', 'EDDM', 'Munich Airport', 'Munich', 'Germany', 48.3537, 11.7860, 'Europe/Berlin'),
    ('BER', 'EDDB', 'Berlin Brandenburg Airport', 'Berlin', 'Germany', 52.3667, 13.5033, 'Europe/Berlin'),
    ('HAM', 'EDDH', 'Hamburg Airport', 'Hamburg', 'Germany', 53.6304, 9.9882, 'Europe/Berlin'),
    ('DUS', 'EDDL', 'Düsseldorf Airport', 'Düsseldorf', 'Germany', 51.2895, 6.7668, 'Europe/Berlin'),
    ('CDG', 'LFPG', 'Charles de Gaulle Airport', 'Paris', 'France', 49.0097, 2.5478, 'Europe/Paris'),
    ('LHR', 'EGLL', 'Heathrow Airport', 'London', 'United Kingdom', 51.4700, -0.4543, 'Europe/London');

-- Insert airlines with various data completeness
INSERT IGNORE INTO airlines (name, iata_code, icao_code, country, active) VALUES
    ('Lufthansa', 'LH', 'DLH', 'Germany', TRUE),
    ('Ryanair', 'FR', 'RYR', 'Ireland', TRUE),
    ('Eurowings', 'EW', 'EWG', 'Germany', TRUE),
    ('Air France', 'AF', 'AFR', 'France', TRUE),
    ('British Airways', 'BA', 'BAW', 'United Kingdom', TRUE);

-- Insert flights with various scenarios
INSERT INTO flights (
    flight_number, 
    airline_id, 
    departure_airport, 
    arrival_airport, 
    scheduled_departure, 
    scheduled_arrival, 
    status, 
    delay_minutes
) VALUES
    -- Regular flights
    ('LH100', 1, 'FRA', 'MUC', NOW() + INTERVAL 2 HOUR, NOW() + INTERVAL 3 HOUR, 'SCHEDULED', 0),
    ('LH101', 1, 'MUC', 'BER', NOW() + INTERVAL 3 HOUR, NOW() + INTERVAL 4 HOUR, 'SCHEDULED', 0),
    ('FR202', 2, 'BER', 'HAM', NOW() - INTERVAL 4 HOUR, NOW() - INTERVAL 3 HOUR, 'DELAYED', 150),
    ('LH103', 1, 'HAM', 'DUS', NOW() - INTERVAL 5 HOUR, NOW() - INTERVAL 4 HOUR, 'DELAYED', 180),
    ('AF123', 4, 'CDG', 'LHR', NOW(), NOW() + INTERVAL 1 HOUR, 'SCHEDULED', 0),
    ('BA456', 5, 'LHR', 'FRA', NOW() + INTERVAL 6 HOUR, NOW() + INTERVAL 7 HOUR, 'SCHEDULED', 0),
    ('LH104', 1, 'FRA', 'CDG', NOW() - INTERVAL 1 HOUR, NOW() + INTERVAL 1 HOUR, 'ACTIVE', 0);

-- Insert status updates with various scenarios
INSERT INTO flight_status_updates (
    flight_id, 
    status, 
    delay_minutes, 
    delay_reason, 
    departure_gate, 
    departure_terminal, 
    arrival_gate, 
    arrival_terminal,
    baggage_claim
) VALUES
    -- Regular status updates
    (3, 'DELAYED', 150, 'Technical issues', 'A12', 'T1', NULL, NULL, NULL),
    (4, 'DELAYED', 180, 'Weather conditions', 'B15', 'T2', NULL, NULL, NULL),
    -- Status update with minimal data
    (5, 'SCHEDULED', 0, NULL, NULL, NULL, NULL, NULL, NULL),
    -- Active flight status
    (7, 'ACTIVE', 0, NULL, 'C10', 'T1', 'D15', 'T2', 'B12'),
    -- Multiple updates for same flight
    (1, 'SCHEDULED', 0, NULL, 'A01', 'T1', NULL, NULL, NULL),
    (1, 'ACTIVE', 15, 'Air traffic control', 'A01', 'T1', NULL, NULL, NULL); 