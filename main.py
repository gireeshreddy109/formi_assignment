from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from haversine import haversine
from rapidfuzz import fuzz, process
import time
from fastapi import FastAPI

app = FastAPI()
@app.get("/greet")
def greet(name: str = Query(..., description="Your name")):
    return {"message": f"Hello, {name}!"}



# Property data
properties = [
    {"name": "Moustache Udaipur Luxuria", "lat": 24.57799888, "lon": 73.68263271},
    {"name": "Moustache Udaipur", "lat": 24.58145726, "lon": 73.68223671},
    {"name": "Moustache Udaipur Verandah", "lat": 24.58350565, "lon": 73.68120777},
    {"name": "Moustache Jaipur", "lat": 27.29124839, "lon": 75.89630143},
    {"name": "Moustache Jaisalmer", "lat": 27.20578572, "lon": 70.85906998},
    {"name": "Moustache Jodhpur", "lat": 26.30365556, "lon": 73.03570908},
    {"name": "Moustache Agra", "lat": 27.26156953, "lon": 78.07524716},
    {"name": "Moustache Delhi", "lat": 28.61257139, "lon": 77.28423582},
    {"name": "Moustache Rishikesh Luxuria", "lat": 30.13769036, "lon": 78.32465767},
    {"name": "Moustache Rishikesh Riverside Resort", "lat": 30.10216117, "lon": 78.38458848},
    {"name": "Moustache Hostel Varanasi", "lat": 25.2992622, "lon": 82.99691388},
    {"name": "Moustache Goa Luxuria", "lat": 15.6135195, "lon": 73.75705228},
    {"name": "Moustache Koksar Luxuria", "lat": 32.4357785, "lon": 77.18518717},
    {"name": "Moustache Daman", "lat": 20.41486263, "lon": 72.83282455},
    {"name": "Panarpani Retreat", "lat": 22.52805539, "lon": 78.43116291},
    {"name": "Moustache Pushkar", "lat": 26.48080513, "lon": 74.5613783},
    {"name": "Moustache Khajuraho", "lat": 24.84602104, "lon": 79.93139381},
    {"name": "Moustache Manali", "lat": 32.28818695, "lon": 77.17702523},
    {"name": "Moustache Bhimtal Luxuria", "lat": 29.36552248, "lon": 79.53481747},
    {"name": "Moustache Srinagar", "lat": 34.11547314, "lon": 74.88701741},
    {"name": "Moustache Ranthambore Luxuria", "lat": 26.05471373, "lon": 76.42953726},
    {"name": "Moustache Coimbatore", "lat": 11.02064612, "lon": 76.96293531},
    {"name": "Moustache Shoja", "lat": 31.56341267, "lon": 77.36733331},
]

# Geocoder setup
geolocator = Nominatim(user_agent="moustache_finder")

class LocationQuery(BaseModel):
    location: str

@app.post("/nearest-property/")
def find_nearest_property(query: LocationQuery):
    start_time = time.time()

    try:
        # Spelling correction using fuzzy matching
        possible_locations = [
            "Delhi", "Udaipur", "Jaipur", "Jaisalmer", "Jodhpur", "Agra", "Rishikesh", "Varanasi",
            "Goa", "Koksar", "Daman", "Pushkar", "Khajuraho", "Manali", "Bhimtal", "Srinagar",
            "Ranthambore", "Coimbatore", "Shoja", "Sissu", "Panarpani"
        ]

        corrected, score, _ = process.extractOne(query.location, possible_locations, scorer=fuzz.token_sort_ratio)
        if score < 70:
            raise HTTPException(status_code=404, detail="Could not understand the location")

        # Geocode corrected location
        try:
            loc = geolocator.geocode(corrected, timeout=10)
        except (GeocoderTimedOut, GeocoderUnavailable):
            raise HTTPException(status_code=503, detail="Geocoding service unavailable")

        if not loc:
            raise HTTPException(status_code=404, detail="Location not found")

        input_coords = (loc.latitude, loc.longitude)

        # Find nearest property
        nearest = None
        min_dist = float('inf')

        for prop in properties:
            prop_coords = (prop["lat"], prop["lon"])
            dist = haversine(input_coords, prop_coords)
            if dist <= 50.0 and dist < min_dist:
                min_dist = dist
                nearest = prop

        response_time = round(time.time() - start_time, 3)

        if nearest:
            return {
                "input_query": query.location,
                "corrected_location": corrected,
                "nearest_property": nearest["name"],
                "distance_km": round(min_dist, 2),
                "response_time_sec": response_time
            }
        else:
            return {
                "input_query": query.location,
                "corrected_location": corrected,
                "message": "No properties found within 50km.",
                "response_time_sec": response_time
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
