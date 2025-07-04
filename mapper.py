"""Generate an interactive map of points of interest near a location.

The script queries OpenStreetMap's Overpass API for several categories of
points of interest (POIs) around a configured address. Results are cached so
subsequent runs are fast. An HTML map is produced with clustered markers for
each POI type. Optional natural features such as rivers, national parks,
hiking trails and related amenities can be included by setting the
``DISPLAY_NATURE`` environment variable to ``true``.
"""

import os
import json
import folium
import requests
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

# Configuration
ADDRESS = "30 Dollar Road, Chapel Hill NC"
RADIUS_KM = 10
POI_TYPES = {
    "grocery": ["supermarket", "grocery"],
    "gym": ["fitness", "gym"],
    "restaurant": ["restaurant", "fast_food", "cafe"],
    "coffee": ["cafe"],
    "bookstore": ["books"],
    "park": ["park", "recreation_ground"],
    "pharmacy": ["pharmacy"],
    "gas": ["fuel"],
    "atm": ["atm"],
    "hardware": ["doityourself", "hardware"],
}

# Optional natural feature categories which can be toggled on or off
NATURE_POI_TYPES = {
    "natural_park": [
        {"key": "leisure", "value": "park"},
        {"key": "boundary", "value": "national_park"},
    ],
    "river": [{"key": "waterway", "value": "river"}],
    "outdoor_activity": [
        {"key": "leisure", "value": "pitch"},
        {"key": "leisure", "value": "sports_centre"},
    ],
    "hiking_trail": [{"key": "highway", "value": "path"}],
    "trailhead": [{"key": "information", "value": "trailhead"}],
    "parking": [{"key": "amenity", "value": "parking"}],
}

# Toggle for displaying natural feature categories
DISPLAY_NATURE = os.getenv("DISPLAY_NATURE", "false").lower() == "true"

if DISPLAY_NATURE:
    POI_TYPES.update(NATURE_POI_TYPES)

# Distinct colors for each POI category used on the map
CATEGORY_COLORS = {
    "grocery": "green",
    "gym": "red",
    "restaurant": "orange",
    "coffee": "lightred",
    "bookstore": "cadetblue",
    "park": "darkgreen",
    "pharmacy": "purple",
    "gas": "gray",
    "atm": "blue",
    "hardware": "darkblue",
}

if DISPLAY_NATURE:
    CATEGORY_COLORS.update(
        {
            "natural_park": "green",
            "river": "blue",
            "outdoor_activity": "lightgreen",
            "hiking_trail": "pink",
            "trailhead": "lightblue",
            "parking": "beige",
        }
    )
CACHE_PATH = "cache/pois.json"
OUTPUT_HTML = "output/map.html"

# Ensure directories exist
os.makedirs("cache", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Geocode home address
if os.getenv("SKIP_GEO", "false").lower() == "true":
    HOME_COORDS = (0.0, 0.0)
else:
    geolocator = Nominatim(user_agent="poi_mapper")
    location = geolocator.geocode(ADDRESS)
    HOME_COORDS = (location.latitude, location.longitude)


# Build Overpass query
def build_query(lat, lon, radius_km, tags):
    """Return an Overpass API query string for the given search parameters.

    ``tags`` may contain amenity strings (legacy) or dictionaries specifying
    arbitrary key/value pairs.
    """

    filter_parts = []
    for tag in tags:
        if isinstance(tag, str):
            filter_parts.append(
                f'node["amenity"="{tag}"](around:{radius_km * 1000},{lat},{lon});'
            )
        else:
            key, value = tag["key"], tag["value"]
            filter_parts.append(
                f'node["{key}"="{value}"](around:{radius_km * 1000},{lat},{lon});'
            )

    filters = "".join(filter_parts)
    return f"[out:json];({filters});out center;"


# Query Overpass API
def fetch_pois():
    """Fetch POIs for each category from Overpass API."""

    all_results = []
    for category, tags in POI_TYPES.items():
        print(f"Fetching {category}...")
        query = build_query(HOME_COORDS[0], HOME_COORDS[1], RADIUS_KM, tags)
        res = requests.post(
            "http://overpass-api.de/api/interpreter", data={"data": query}
        )
        data = res.json()
        for el in data.get("elements", []):
            all_results.append(
                {
                    "type": category,
                    "name": el.get("tags", {}).get("name", "Unnamed"),
                    "lat": el["lat"],
                    "lon": el["lon"],
                }
            )
    return all_results


# Load or fetch data
def main():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            pois = json.load(f)
    else:
        pois = fetch_pois()
        with open(CACHE_PATH, "w") as f:
            json.dump(pois, f)

    # Build map
    m = folium.Map(location=HOME_COORDS, zoom_start=13)
    folium.Marker(
        HOME_COORDS, tooltip="Home", icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)
    marker_cluster = MarkerCluster().add_to(m)

    for poi in pois:
        color = CATEGORY_COLORS.get(poi["type"], "lightgray")
        folium.Marker(
            [poi["lat"], poi["lon"]],
            tooltip=f"{poi['name']} ({poi['type']})",
            popup=folium.Popup(
                f"<b>{poi['name']}</b><br/>Type: {poi['type']}", parse_html=True
            ),
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(marker_cluster)

    m.save(OUTPUT_HTML)
    print(f"Map saved to {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
