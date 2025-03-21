 -- Basic queries to view table contents
SELECT * FROM airports ORDER BY country, city;

-- View all airlines and their flight counts
SELECT 
    a.name AS airline_name,
    a.iata_code,
    COUNT(f.flight_id) AS total_flights
FROM airlines a
LEFT JOIN flights f ON a.airline_id = f.airline_id
GROUP BY a.airline_id, a.name, a.iata_code
ORDER BY total_flights DESC;

-- View all delayed flights with airline and airport info
SELECT 
    f.flight_number,
    al.name AS airline,
    dep.city AS departure_city,
    arr.city AS arrival_city,
    f.scheduled_departure,
    f.delay_minutes,
    f.status
FROM flights f
JOIN airlines al ON f.airline_id = al.airline_id
JOIN airports dep ON f.departure_airport = dep.iata_code
JOIN airports arr ON f.arrival_airport = arr.iata_code
WHERE f.delay_minutes > 0
ORDER BY f.delay_minutes DESC;

-- View flight status distribution
SELECT 
    f.status,
    COUNT(*) as flight_count,
    AVG(f.delay_minutes) as avg_delay
FROM flights f
GROUP BY f.status
ORDER BY flight_count DESC;

-- View airports with most departures
SELECT 
    a.name AS airport_name,
    a.city,
    a.country,
    COUNT(f.flight_id) AS departure_count
FROM airports a
LEFT JOIN flights f ON a.iata_code = f.departure_airport
GROUP BY a.iata_code, a.name, a.city, a.country
ORDER BY departure_count DESC;

-- View recent flight status updates
SELECT 
    f.flight_number,
    al.name AS airline,
    fsu.status,
    fsu.delay_minutes,
    fsu.delay_reason,
    fsu.status_update_time
FROM flight_status_updates fsu
JOIN flights f ON fsu.flight_id = f.flight_id
JOIN airlines al ON f.airline_id = al.airline_id
ORDER BY fsu.status_update_time DESC
LIMIT 10;

-- View flights with multiple status changes
SELECT 
    f.flight_number,
    al.name AS airline,
    COUNT(fsu.update_id) AS status_change_count,
    GROUP_CONCAT(DISTINCT fsu.status) AS status_sequence
FROM flights f
JOIN airlines al ON f.airline_id = al.airline_id
JOIN flight_status_updates fsu ON f.flight_id = fsu.flight_id
GROUP BY f.flight_id, f.flight_number, al.name
HAVING COUNT(fsu.update_id) > 1
ORDER BY status_change_count DESC;

-- View average delays by route
SELECT 
    dep.city AS departure_city,
    arr.city AS arrival_city,
    COUNT(*) AS flight_count,
    AVG(f.delay_minutes) AS avg_delay,
    MAX(f.delay_minutes) AS max_delay
FROM flights f
JOIN airports dep ON f.departure_airport = dep.iata_code
JOIN airports arr ON f.arrival_airport = arr.iata_code
GROUP BY dep.city, arr.city
HAVING flight_count > 1
ORDER BY avg_delay DESC;