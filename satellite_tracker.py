import argparse
import json
from config import SATELLITES, DEFAULT_ELEV, DEFAULT_TIME, API_KEY
from n2yo_service import get_satellite_passes, NORAD_to_name
from formatting_service import format_time, city_to_coords


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
        default=DEFAULT_TIME,
        help="Days to scrap ahead"
    )
    parser.add_argument(
        "-e", "--min-elevation",
        type=float,
        default=DEFAULT_ELEV,
        help="Minimum elevation in degrees"
    )
    parser.add_argument(
        "-s", "--satellite-ids",
        default=list(SATELLITES.keys()),
        nargs="*",
        type=int,
        help="Specific satellite to track"
    )

    args = parser.parse_args()

    # Check whether coordinates or city was given in args.location
    lat, lon = None, None
    if "," in args.location:
        try:
            lat, lon = map(float, args.location.split(","))
        except ValueError:
            pass
    
    if lat is None:
        location_name = args.location

        lat, lon = city_to_coords(args.location)
        if lat is None:
            print(f"Error: City '{location_name}' was not found")
            return
    
    # Find passes
    all_passes = []
    
    for sat_id in args.satellite_ids:
        passes = get_satellite_passes(
            lat=lat, 
            lon=lon, 
            satellite_id=sat_id, 
            days=args.days, 
            min_elevation=args.min_elevation, 
            api_key=API_KEY
        )

        sat_name = SATELLITES.get(sat_id)

        if sat_name is None:
            sat_name = NORAD_to_name(sat_id, API_KEY)
        
        for i in passes:
            i["sat_info"] = f"{sat_name} ({sat_id})"
 
        all_passes.extend(passes)

    sorted_passes = sorted(all_passes, key=lambda i: i["startUTC"])
    
    #Cleaning data
    for i in sorted_passes:
        i["duration"] = f"{(i["endUTC"] - i["startUTC"]) // 60}m {(i["endUTC"] - i["startUTC"]) % 60}s"
        i["startUTC"] = format_time(i.get("startUTC"))
        i["maxUTC"] = format_time(i.get("maxUTC"))
        i["endUTC"] = format_time(i.get("endUTC"))
    
    print("Satellite Tracker v1.0")
    print("=" * 40)
    print(f"Location: {args.location} ({lat}, {lon})")
    print(f"Looking ahead: {args.days} days")
    print(f"Minimum elevation: {args.min_elevation}°")
    print(f"Satellites tracked: {', '.join(set(i.get('sat_info') for i in sorted_passes))}")
    print("=" * 40)
    print(f"Found {len(sorted_passes)} passes:\n")
    print(json.dumps(sorted_passes, indent=2))


if __name__ == "__main__":
    main()
