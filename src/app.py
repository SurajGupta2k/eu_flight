from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from database.models import db, Airport, Airline, Flight, FlightStatus, FlightStatusUpdate
from api.aviation_service import AviationService
from datetime import datetime, timedelta
import os
import json

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load airport data from JSON file
    with open(os.path.join(os.path.dirname(__file__), 'data/airports.json')) as f:
        AIRPORT_DATA = json.load(f)

    # Configure MySQL database connection with PyMySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Flask extensions
    db.init_app(app)
    aviation_service = AviationService()

    def init_flight_statuses():
        """Initialize flight status values if they don't exist"""
        statuses = ['SCHEDULED', 'ACTIVE', 'LANDED', 'CANCELLED', 'DIVERTED', 'DELAYED']
        for status in statuses:
            if not FlightStatus.query.get(status):
                db.session.add(FlightStatus(status=status))
        db.session.commit()

    @app.route('/', methods=['GET'])
    def read_root():
        """Read Root - API Documentation"""
        return render_template('docs.html'), 200, {'Content-Type': 'text/html'}

    @app.route('/openapi.json', methods=['GET'])
    def openapi_json():
        """OpenAPI Specification"""
        return jsonify({
            "openapi": "3.1",
            "paths": {
                "/": {
                    "get": {
                        "summary": "Read Root",
                        "description": "Read Root",
                        "tags": ["default"],
                        "parameters": [],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/airports": {
                    "get": {
                        "summary": "Get Airports",
                        "description": "Get list of all airports",
                        "tags": ["default"],
                        "parameters": [],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/airports/{airport_code}/flights": {
                    "get": {
                        "summary": "Get Airport Flights",
                        "description": "Get all flights from a specific airport",
                        "tags": ["default"],
                        "parameters": [
                            {
                                "name": "airport_code",
                                "in": "path",
                                "required": true,
                                "schema": {
                                    "type": "string"
                                },
                                "description": "airport_code"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "detail": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "loc": {
                                                                "type": "array",
                                                                "items": {}
                                                            },
                                                            "msg": {"type": "string"},
                                                            "type": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/flights/delayed": {
                    "get": {
                        "summary": "Get Delayed Flight List",
                        "description": "Get all flights delayed by more than 2 hours",
                        "tags": ["default"],
                        "parameters": [],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/flights/{flight_id}": {
                    "get": {
                        "summary": "Get Flight Details",
                        "description": "Get details for a specific flight",
                        "tags": ["default"],
                        "parameters": [
                            {
                                "name": "flight_id",
                                "in": "path",
                                "required": true,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "flight_id"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "detail": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "loc": {
                                                                "type": "array",
                                                                "items": {}
                                                            },
                                                            "msg": {"type": "string"},
                                                            "type": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/flights/active": {
                    "get": {
                        "summary": "Get Active Flight List",
                        "description": "Get all currently active flights",
                        "tags": ["default"],
                        "parameters": [],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/flights/search/{flight_number}": {
                    "get": {
                        "summary": "Search Flight",
                        "description": "Search for real-time flight information using Aviation Stack API",
                        "tags": ["default"],
                        "parameters": [
                            {
                                "name": "flight_number",
                                "in": "path",
                                "required": true,
                                "schema": {
                                    "type": "string"
                                },
                                "description": "flight_number"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "string"}
                                    }
                                }
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "detail": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "loc": {
                                                                "type": "array",
                                                                "items": {}
                                                            },
                                                            "msg": {"type": "string"},
                                                            "type": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/flights/live": {
                    "get": {
                        "summary": "Get Live Flights",
                        "description": "Get live flight data with optional filtering",
                        "tags": ["default"],
                        "parameters": [
                            {
                                "name": "airline",
                                "in": "query",
                                "required": false,
                                "schema": {
                                    "type": "string"
                                },
                                "description": "Filter by airline IATA code"
                            },
                            {
                                "name": "limit",
                                "in": "query",
                                "required": false,
                                "schema": {
                                    "type": "integer",
                                    "default": 100
                                },
                                "description": "Limit the number of results"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "Unauthorized - Invalid API key",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "error": {
                                                    "type": "string"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "tags": [
                {
                    "name": "default",
                    "description": "Default endpoints"
                }
            ],
            "title": "EU Flight Monitor",
            "version": "1.0.0"
        })

    @app.route('/airports', methods=['GET'])
    def get_airports():
        """Get list of all airports"""
        try:
            airports = Airport.query.all()
            return jsonify([{
                'iata_code': a.iata_code,
                'name': a.name,
                'city': a.city,
                'country': a.country,
                'latitude': a.latitude,
                'longitude': a.longitude
            } for a in airports])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/airports/<airport_code>/flights', methods=['GET'])
    def get_airport_flights(airport_code):
        """Get flights for a specific airport"""
        try:
            date = request.args.get('date', datetime.now().date().isoformat())
            
            # Query flights departing or arriving at this airport on given date
            flights = Flight.query.join(Airline)\
                .filter(
                    (Flight.departure_airport == airport_code) | 
                    (Flight.arrival_airport == airport_code)
                )\
                .filter(db.func.date(Flight.scheduled_departure) == date)\
                .all()

            return jsonify([{
                'flight_id': f.flight_id,
                'flight_number': f.flight_number,
                'airline': f.airline.name,
                'departure': f.departure_airport,
                'arrival': f.arrival_airport,
                'scheduled_departure': f.scheduled_departure.isoformat(),
                'status': f.status
            } for f in flights])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/flights/delayed', methods=['GET'])
    def get_delayed_flights():
        """Get flights delayed by more than 2 hours"""
        try:
            delayed_flights = Flight.query.join(Airline)\
                .filter(Flight.delay_minutes >= 120)\
                .all()

            return jsonify([{
                'flight_id': f.flight_id,
                'flight_number': f.flight_number,
                'airline': f.airline.name,
                'departure': f.departure_airport,
                'arrival': f.arrival_airport,
                'scheduled_departure': f.scheduled_departure.isoformat(),
                'delay_minutes': f.delay_minutes,
                'status': f.status
            } for f in delayed_flights])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/flights/<int:flight_id>', methods=['GET'])
    def get_flight_details(flight_id):
        """Get detailed information for a specific flight"""
        try:
            # Get flight and its latest status update
            flight = Flight.query.get_or_404(flight_id)
            latest_update = FlightStatusUpdate.query\
                .filter_by(flight_id=flight_id)\
                .order_by(FlightStatusUpdate.status_update_time.desc())\
                .first()

            return jsonify({
                'flight_id': flight.flight_id,
                'flight_number': flight.flight_number,
                'airline': {
                    'name': flight.airline.name,
                    'iata_code': flight.airline.iata_code
                },
                'departure': {
                    'airport': flight.departure_airport_info.name,
                    'iata': flight.departure_airport,
                    'scheduled': flight.scheduled_departure.isoformat(),
                    'actual': latest_update.actual_departure.isoformat() if latest_update and latest_update.actual_departure else None,
                    'gate': latest_update.departure_gate if latest_update else None,
                    'terminal': latest_update.departure_terminal if latest_update else None
                },
                'arrival': {
                    'airport': flight.arrival_airport_info.name,
                    'iata': flight.arrival_airport,
                    'scheduled': flight.scheduled_arrival.isoformat() if flight.scheduled_arrival else None,
                    'gate': latest_update.arrival_gate if latest_update else None,
                    'terminal': latest_update.arrival_terminal if latest_update else None
                },
                'status': flight.status,
                'delay_minutes': flight.delay_minutes
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/flights/active', methods=['GET'])
    def get_active_flights():
        """Get currently active flights"""
        try:
            active_flights = Flight.query.join(Airline)\
                .filter(Flight.status == 'ACTIVE')\
                .all()

            return jsonify([{
                'flight_id': f.flight_id,
                'flight_number': f.flight_number,
                'airline': f.airline.name,
                'departure': f.departure_airport,
                'arrival': f.arrival_airport,
                'scheduled_departure': f.scheduled_departure.isoformat(),
                'status': f.status
            } for f in active_flights])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/flights/search/<flight_number>', methods=['GET'])
    def search_flight(flight_number):
        """Search for a specific flight by number"""
        try:
            # Get most recent flight with this number
            flight = Flight.query.filter_by(flight_number=flight_number)\
                .order_by(Flight.scheduled_departure.desc())\
                .first()

            if not flight:
                return jsonify({'error': 'Flight not found'}), 404

            return jsonify({
                'flight_id': flight.flight_id,
                'flight_number': flight.flight_number,
                'airline': flight.airline.name,
                'departure': flight.departure_airport,
                'arrival': flight.arrival_airport,
                'scheduled_departure': flight.scheduled_departure.isoformat(),
                'status': flight.status,
                'delay_minutes': flight.delay_minutes
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/flights/live', methods=['GET'])
    def get_live_flights():
        """Get real-time flight data"""
        try:
            airline = request.args.get('airline')
            limit = request.args.get('limit', 100, type=int)
            
            # Get live flight data from aviation service
            flights = aviation_service.get_live_flights(limit=limit)
            
            # Filter by airline if specified
            if airline:
                flights['data'] = [f for f in flights['data'] 
                                 if f.get('airline', {}).get('iata') == airline]
            
            # Store flight data in database
            for flight_data in flights['data']:
                store_flight_data(flight_data)
            
            return jsonify(flights)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def enrich_airport_data(airport_info):
        """Add additional airport info from local database"""
        iata = airport_info.get('iata')
        if iata and iata in AIRPORT_DATA:
            supplementary_data = AIRPORT_DATA[iata]
            return {
                'iata_code': iata,
                'name': airport_info.get('airport', supplementary_data['name']),
                'city': supplementary_data['city'],
                'country': supplementary_data['country'],
                'latitude': supplementary_data['latitude'],
                'longitude': supplementary_data['longitude'],
                'timezone': supplementary_data['timezone']
            }
        return {
            'iata_code': iata,
            'name': airport_info.get('airport', f"Airport {iata}"),
            'city': airport_info.get('city', 'Unknown'),
            'country': airport_info.get('country', 'Unknown'),
            'latitude': None,
            'longitude': None,
            'timezone': None
        }

    def store_flight_data(flight_data):
        """Store flight data in database"""
        try:
            # Get or create airline record
            airline_info = flight_data.get('airline', {})
            airline = Airline.query.filter_by(iata_code=airline_info.get('iata')).first()
            if not airline and airline_info.get('iata'):
                airline = Airline(
                    name=airline_info.get('name', f"Airline {airline_info.get('iata')}"),
                    iata_code=airline_info.get('iata'),
                    icao_code=airline_info.get('icao'),
                    country=airline_info.get('country', 'Unknown'),
                    active=True
                )
                db.session.add(airline)
                db.session.flush()
            elif not airline:
                return

            # Create airport records if needed
            dep_info = flight_data.get('departure', {})
            arr_info = flight_data.get('arrival', {})
            
            for airport_info in [dep_info, arr_info]:
                iata = airport_info.get('iata')
                if iata and not Airport.query.get(iata):
                    enriched_data = enrich_airport_data(airport_info)
                    airport = Airport(**enriched_data)
                    db.session.add(airport)

            # Create or update flight record
            flight_number = flight_data.get('flight', {}).get('number')
            if not flight_number:
                return
                
            scheduled_dep = dep_info.get('scheduled')
            if not scheduled_dep:
                return

            flight = Flight.query.filter_by(
                flight_number=flight_number,
                scheduled_departure=datetime.fromisoformat(scheduled_dep)
            ).first()

            if not flight:
                flight = Flight(
                    flight_number=flight_number,
                    airline_id=airline.airline_id,
                    departure_airport=dep_info.get('iata'),
                    arrival_airport=arr_info.get('iata'),
                    scheduled_departure=datetime.fromisoformat(scheduled_dep),
                    scheduled_arrival=datetime.fromisoformat(arr_info.get('scheduled', scheduled_dep)),
                    status='SCHEDULED'
                )
                db.session.add(flight)
                db.session.flush()

            # Create status update record
            status_update = FlightStatusUpdate(
                flight_id=flight.flight_id,
                status=flight_data.get('flight_status', 'SCHEDULED').upper(),
                actual_departure=dep_info.get('actual'),
                estimated_departure=dep_info.get('estimated'),
                delay_minutes=dep_info.get('delay'),
                departure_gate=dep_info.get('gate'),
                departure_terminal=dep_info.get('terminal'),
                arrival_gate=arr_info.get('gate'),
                arrival_terminal=arr_info.get('terminal')
            )
            db.session.add(status_update)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

    @app.route('/api/flights/search', methods=['GET'])
    def search_flights():
        """Search flights with filters"""
        try:
            params = {
                'flight_number': request.args.get('flight'),
                'airline_code': request.args.get('airline'),
                'dep_iata': request.args.get('departure'),
                'arr_iata': request.args.get('arrival')
            }
            
            flights = aviation_service.search_flights(**params)
            return jsonify(flights)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/stats/delays', methods=['GET'])
    def get_delay_stats():
        """Get airline delay statistics"""
        try:
            # Calculate average delays by airline
            stats = db.session.query(
                Airline.name,
                db.func.avg(Flight.delay_minutes).label('avg_delay'),
                db.func.count(Flight.flight_id).label('total_flights')
            ).join(Flight).group_by(Airline.name).all()

            return jsonify([{
                'airline': s.name,
                'avg_delay': float(s.avg_delay or 0),
                'total_flights': s.total_flights
            } for s in stats])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/flights/<flight_id>/history', methods=['GET'])
    def get_flight_history(flight_id):
        """Get flight status history"""
        try:
            # Get all status updates for flight
            updates = FlightStatusUpdate.query.filter_by(flight_id=flight_id)\
                .order_by(FlightStatusUpdate.status_update_time.desc()).all()
            
            return jsonify([{
                'status': u.status,
                'update_time': u.status_update_time.isoformat(),
                'delay_minutes': u.delay_minutes,
                'delay_reason': u.delay_reason,
                'departure_gate': u.departure_gate,
                'arrival_gate': u.arrival_gate
            } for u in updates])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/airports/european', methods=['GET'])
    def get_european_airports():
        """Get European airports"""
        try:
            # List of EU countries plus Norway and Switzerland
            european_countries = [
                'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
                'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
                'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
                'Spain', 'Sweden', 'United Kingdom', 'Norway', 'Switzerland'
            ]
            
            airports = Airport.query.filter(Airport.country.in_(european_countries)).all()
            
            return jsonify([{
                'name': a.name,
                'iata_code': a.iata_code,
                'city': a.city,
                'country': a.country,
                'latitude': a.latitude,
                'longitude': a.longitude
            } for a in airports])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Initialize database and flight statuses
    with app.app_context():
        db.create_all()
        init_flight_statuses()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 