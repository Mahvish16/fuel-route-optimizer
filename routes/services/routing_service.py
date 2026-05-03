import requests


STATE_NAME_TO_CODE = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


def geocode_location(location):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{location}, USA",
        "format": "json",
        "limit": 1,
        "countrycodes": "us"
    }

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "fuel-route-optimizer"}
    )

    data = response.json()

    if not data:
        raise ValueError(f"Location not found: {location}")

    return {
        "lat": float(data[0]["lat"]),
        "lng": float(data[0]["lon"])
    }


def reverse_geocode_state(lat, lng):
    url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "lat": lat,
        "lon": lng,
        "format": "json",
        "zoom": 5
    }

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "fuel-route-optimizer"}
    )

    data = response.json()
    address = data.get("address", {})
    state_name = address.get("state")

    return STATE_NAME_TO_CODE.get(state_name)


def detect_route_states(coordinates, sample_count=6):
    """
    Detect states from route coordinates.
    We sample only a few points to keep the API fast.
    """

    if not coordinates:
        return []

    states = []

    total_points = len(coordinates)

    if total_points <= sample_count:
        sampled_points = coordinates
    else:
        sampled_points = []
        for i in range(sample_count):
            index = round(i * (total_points - 1) / (sample_count - 1))
            sampled_points.append(coordinates[index])

    for point in sampled_points:
        lng = point[0]
        lat = point[1]

        state_code = reverse_geocode_state(lat, lng)

        if state_code and state_code not in states:
            states.append(state_code)

    return states


def get_route(start_location, finish_location):
    start = geocode_location(start_location)
    finish = geocode_location(finish_location)

    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start['lng']},{start['lat']};{finish['lng']},{finish['lat']}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError("Unable to fetch route")

    route = data["routes"][0]
    coordinates = route["geometry"]["coordinates"]

    route_states = detect_route_states(coordinates)

    return {
        "distance_miles": route["distance"] / 1609.34,
        "duration_minutes": route["duration"] / 60,
        "geometry": route["geometry"],
        "start_coordinates": start,
        "finish_coordinates": finish,
        "route_states": route_states
    }