import argparse
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.environ.get("N2YO_API_KEY")

SATELLITES = {
    "ISS": 25544,
    "NOAA 19": 33591,
    "NOAA 18": 28654,
    "NOAA 15": 25338,
    "METOP-B": 38771,
    "METOP-C": 43689,
    "AQUA": 27424,
    "TERRA": 25994,
    "SUOMI NPP": 37849,
    "ENVISAT": 27386,
    "LANDSAT 8": 39084
}

def get_satellite_passes(lat, lon, satellite_id, days, min_elevation, api_key):
    """Fetch satellite data from N2YO API"""
    url = f"https://api.n2yo.com/rest/v1/satellite/radiopasses/{satellite_id}/{lat}/{lon}/0/{days}/{min_elevation}"

    response = requests.get(url, params={"apiKey": api_key})
    
    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        return []
    
    data = response.json()
    
    return data.get("passes", [])

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S UTC %b/%d/%Y")
    
def main():
    parser = argparse.ArgumentParser(description="Track satellites in passes")
    
    # arguments
    parser.add_argument(
        "-l", "--location",
        required=True, 
        type=str,
        help="City name or coordinates (lat,lon), as str"
    )
    parser.add_argument(
        "-d", "--days", 
        type=int, 
        default=7,
        help="Days to scrap ahead"
    )
    parser.add_argument(
        "-e", "--min-elevation",
        type=float,
        default=30,
        help="Minimum elevation in degrees"
    )
    parser.add_argument(
        "-s", "--satellite-ids",
        default=None,
        nargs="*",
        type=int,
        help="Specific satellite to track"
    )

    args = parser.parse_args()
    
    print("Satellite Tracker v1.0")
    print("=" * 40)
    print(f"Location: {args.location}")
    print(f"Looking ahead: {args.days} days")
    print(f"Minimum elevation: {args.min_elevation}°")
    

    if args.satellite_ids == None or len(args.satellite_ids) == 0:
        satellite_ids = list(SATELLITES.values())
        print(f"Tracking all {len(satellite_ids)} major satellites")
    else:
        satellite_ids = args.satellite_ids
        print(f"Tracking {len(satellite_ids)} specific satellite(s)") 
    print("=" * 40)

    lat, lon = map(float, args.location.split(","))
    
    all_passes = []
    
    for sat_id in satellite_ids:
        passes = get_satellite_passes(
            lat=lat, 
            lon=lon, 
            satellite_id=sat_id, 
            days=args.days, 
            min_elevation=args.min_elevation, 
            api_key=API_KEY
        )
        for i in passes:
            i["sat_id"] = sat_id
            
        all_passes.extend(passes)

    sorted_passes = sorted(all_passes, key=lambda i: i["startUTC"])
    
    #Cleaning data
    for i in sorted_passes:
        i["duration"] = f"{(i["endUTC"] - i["startUTC"]) // 60}m {(i["endUTC"] - i["startUTC"]) % 60}s"
        i["startUTC"] = format_time(i.get("startUTC"))
        i["maxUTC"] = format_time(i.get("maxUTC"))
        i["endUTC"] = format_time(i.get("endUTC"))
    
    print(f"Found {len(sorted_passes)} passes:\n")
    print(json.dumps(sorted_passes, indent=2))


if __name__ == "__main__":
    main()
