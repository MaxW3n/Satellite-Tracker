import requests
from datetime import datetime
from config import NOMINATIM_BASE_URL

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S UTC %b/%d/%Y")

def city_to_coords(city):
    """Convert city names to decimal coordinates."""
    url=f"{NOMINATIM_BASE_URL}/search"
    
    headers = {"User-Agent": "SatelliteTracker/1.0"}
    
    response = requests.get(url, 
        params={
            "q": city, 
            "format": "json",
            "limit": 1},
        headers=headers
    )

    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        return None, None
    
    data = response.json()

    if not data:
        return None, None
    
    coords = data[0]
    return coords["lat"], coords["lon"]