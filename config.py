"""Configuration and constants for satellite tracker."""
import os
from dotenv import load_dotenv

# N2YO API key
load_dotenv()
API_KEY = os.environ.get("N2YO_API_KEY")

# URLs
N2YO_BASE_URL = 'https://api.n2yo.com/rest/v1'
NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org'

# Constants
SATELLITES = {
    25544: "ISS",
    33591: "NOAA 19",
    28654: "NOAA 18",
    25338: "NOAA 15",
    38771: "METOP-B",
    43689: "METOP-C",
    27424: "AQUA",
    25994: "TERRA",
    37849: "SUOMI NPP",
    27386: "ENVISAT",
    39084: "LANDSAT 8"
}

DEFAULT_ELEV = 30 # in degrees
DEFAULT_TIME = 7 # in days
