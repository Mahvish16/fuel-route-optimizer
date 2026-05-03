# Fuel Route Optimizer API

Django REST Framework API that takes a start and finish location in the USA, calculates the route, finds cost-effective fuel stops using the provided fuel price CSV, and returns total estimated fuel cost.

## Features

- Accepts start and finish locations
- Uses OSRM for route/map GeoJSON
- Uses Nominatim for geocoding locations
- Imports provided fuel price CSV into database
- Vehicle range: 500 miles
- Fuel efficiency: 10 MPG
- Returns fuel stops and total fuel cost

## Tech Stack

Python, Django, Django REST Framework, SQLite, Pandas, Requests, OSRM API, Nominatim API

## Setup

```bash
git clone https://github.com/Mahvish16/fuel-route-optimizer.git
cd fuel-route-optimizer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_fuel_prices
python manage.py runserver
```

Server runs at:

```text
http://127.0.0.1:8000/
```

## API Endpoint

```http
POST http://127.0.0.1:8000/api/route/fuel-plan/
```

## Request Body

```json
{
  "start_location": "New York, NY",
  "finish_location": "Chicago, IL"
}
```

## Response Includes

- Route distance and duration
- Route states
- GeoJSON route map data
- Fuel stops
- Gallons needed
- Cost per stop
- Total fuel cost

## How It Works

1. The API geocodes start and finish locations.
2. OSRM returns route distance, duration, and GeoJSON map data.
3. The provided fuel price CSV is imported into the database.
4. Fuel stations are filtered using route states.
5. The route is divided by 500-mile range.
6. Fuel cost is calculated using 10 MPG.

## Assumptions

- Start and finish locations are within the USA.
- Fuel prices come from the provided CSV.
- The CSV does not include latitude/longitude for stations, so optimization is based on route states and fuel prices.
- With exact station coordinates, the next improvement would be selecting stations within a route corridor.

## Test Example

```json
{
  "start_location": "Los Angeles, CA",
  "finish_location": "Las Vegas, NV"
}
```
