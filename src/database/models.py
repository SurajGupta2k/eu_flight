from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Stores valid flight statuses like SCHEDULED, DELAYED, ACTIVE etc
class FlightStatus(db.Model):
    __tablename__ = 'flight_status'
    status = db.Column(db.String(20), primary_key=True)
    flights = db.relationship('Flight', backref='flight_status', foreign_keys='Flight.status')
    status_updates = db.relationship('FlightStatusUpdate', backref='status_info', foreign_keys='FlightStatusUpdate.status')

# Airport information including location and codes
class Airport(db.Model):
    __tablename__ = 'airports'
    iata_code = db.Column(db.String(3), primary_key=True)
    icao_code = db.Column(db.String(4), unique=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.String(50))
    departures = db.relationship('Flight', backref='departure_airport_info', foreign_keys='Flight.departure_airport')
    arrivals = db.relationship('Flight', backref='arrival_airport_info', foreign_keys='Flight.arrival_airport')

# Airlines operating the flights
class Airline(db.Model):
    __tablename__ = 'airlines'
    airline_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    iata_code = db.Column(db.String(2), unique=True)
    icao_code = db.Column(db.String(3), unique=True)
    country = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    flights = db.relationship('Flight', backref='airline')

# Main flight information including schedule and status
class Flight(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.airline_id'), nullable=False)
    departure_airport = db.Column(db.String(3), db.ForeignKey('airports.iata_code'), nullable=False)
    arrival_airport = db.Column(db.String(3), db.ForeignKey('airports.iata_code'), nullable=False)
    scheduled_departure = db.Column(db.DateTime, nullable=False)
    scheduled_arrival = db.Column(db.DateTime)
    actual_departure = db.Column(db.DateTime)
    actual_arrival = db.Column(db.DateTime)
    estimated_departure = db.Column(db.DateTime)
    estimated_arrival = db.Column(db.DateTime)
    status = db.Column(db.String(20), db.ForeignKey('flight_status.status'), nullable=False)
    delay_minutes = db.Column(db.Integer, default=0)
    aircraft_registration = db.Column(db.String(20))
    aircraft_type = db.Column(db.String(50))
    status_updates = db.relationship('FlightStatusUpdate', backref='flight')

# Tracks changes in flight status, delays and gate information
class FlightStatusUpdate(db.Model):
    __tablename__ = 'flight_status_updates'
    update_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False)
    status = db.Column(db.String(20), db.ForeignKey('flight_status.status'), nullable=False)
    status_update_time = db.Column(db.DateTime, default=datetime.utcnow)
    actual_departure = db.Column(db.DateTime)
    estimated_departure = db.Column(db.DateTime)
    delay_minutes = db.Column(db.Integer)
    delay_reason = db.Column(db.String(200))
    departure_gate = db.Column(db.String(10))
    departure_terminal = db.Column(db.String(10))
    arrival_gate = db.Column(db.String(10))
    arrival_terminal = db.Column(db.String(10))
    baggage_claim = db.Column(db.String(20))