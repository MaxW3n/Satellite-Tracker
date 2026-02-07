import requests
from config import N2YO_BASE_URL

def get_satellite_passes(lat, lon, satellite_id, days, min_elevation, api_key):
    """Fetch satellite data from N2YO API"""
    url = f"{N2YO_BASE_URL}/satellite/radiopasses/{satellite_id}/{lat}/{lon}/0/{days}/{min_elevation}"

    response = requests.get(url, params={"apiKey": api_key})
    
    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        return []
    
    data = response.json()
    
    return data.get("passes", [])

def NORAD_to_name(NORAD_id, api_key):
    """Converts NORAD id to satellite name"""
    url = f"{N2YO_BASE_URL}/satellite/tle/{NORAD_id}"

    response = requests.get(url, params={"apiKey": api_key})

    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        return "Unknown"
    
    data = response.json().get("info", {})

    # Debugging
    # print(data)

    return data.get("satname", "Unknown")