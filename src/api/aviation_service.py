import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

class AviationService:
    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv('AVIATION_API_KEY')
        self.base_url = "http://api.aviationstack.com/v1"
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the Aviation Stack API"""
        try:
            url = f"{self.base_url}/{endpoint}"
            params = params or {}
            
            # Make sure we have an API key
            if not self.api_key:
                raise ValueError("Aviation Stack API key is not configured")
            
            params['access_key'] = self.api_key
            
            # Make the API call
            response = requests.get(url, params=params)
            
            # Handle common API errors
            if response.status_code == 401:
                raise ValueError("Invalid API key or unauthorized access")
            elif response.status_code == 429:
                raise ValueError("API rate limit exceeded")
            
            response.raise_for_status()
            data = response.json()
            
            # Check for API-specific errors in response
            if 'error' in data:
                error_info = data['error']
                raise ValueError(f"API Error: {error_info.get('message', 'Unknown error')}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def get_live_flights(self, limit: int = 100) -> List[Dict]:
        """Get live flight data"""
        return self._make_request('flights', {'limit': limit})
    
    def get_airline_routes(self, airline_code: str) -> List[Dict]:
        """Get routes for a specific airline"""
        return self._make_request('routes', {'airline_code': airline_code})
    
    def get_airport_schedules(self, iata_code: str) -> List[Dict]:
        """Get schedules for a specific airport"""
        return self._make_request('schedules', {'dep_iata': iata_code})
    
    def search_flights(self, 
                      flight_number: Optional[str] = None,
                      airline_code: Optional[str] = None,
                      dep_iata: Optional[str] = None,
                      arr_iata: Optional[str] = None) -> List[Dict]:
        """Search for flights with various filters"""
        # Only include non-None parameters in the request
        params = {k: v for k, v in {
            'flight_number': flight_number,
            'airline_code': airline_code,
            'dep_iata': dep_iata,
            'arr_iata': arr_iata
        }.items() if v is not None}
        
        return self._make_request('flights', params)