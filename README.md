# formi_assignment

# Moustache Property Finder API

A FastAPI-based REST API to locate the nearest Moustache property based on a user-provided location. It uses geocoding, fuzzy string matching, and distance computation to determine the closest property from a curated list.

---

## Features

- FastAPI framework for high-performance web service.
- Location correction using RapidFuzz (fuzzy matching).
- Geocoding via geopy + OpenStreetMap (Nominatim).
- Haversine formula for distance calculation.
- Returns nearest Moustache property within a 50 km radius.
- Fast response time with built-in timing.

---

To enhance the user experience, the API intelligently handles spelling mistakes or slightly incorrect location names. 
This is achieved using RapidFuzz, a fast and accurate string matching library based on fuzzy logic. 
When a user submits a location name—even if it's misspelled or partially incorrect—the API uses RapidFuzz to find the 
most relevant match from a predefined list of possible locations. This ensures reliable results even when the input isn't perfectly formatted.

## Requirements

- Python 3.9+
- pip (Python package manager)

### Python Libraries

```bash
pip install fastapi uvicorn geopy haversine rapidfuzz


Start the FastAPI server:
uvicorn main:app --reload

Open in browser:
http://127.0.0.1:8000
{
  "location": "delhi"
}


POST /nearest-property/
Finds the nearest Moustache property to a given location name.

Request body (application/json):

{
  "location": "delhi"
}

Response example:

{
  "input_query": "delhi",
  "corrected_location": "Delhi",
  "nearest_property": "Moustache Delhi",
  "distance_km": 4.37,
  "response_time_sec": 0.534
}

Response if no property is within 50km:

{
  "input_query": "somewhere far",
  "corrected_location": "Unknown",
  "message": "No properties found within 50km.",
  "response_time_sec": 0.5
}


