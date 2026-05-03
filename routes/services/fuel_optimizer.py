import math
from fuel.models import FuelStation

MAX_RANGE_MILES = 500
MILES_PER_GALLON = 10


def get_states_for_segment(route_states, stop_number, total_stops):
    """
    Divide route states into parts so every fuel stop is selected
    from a different section of the route.
    """

    if not route_states:
        return []

    if total_stops == 1:
        return route_states

    states_per_segment = max(1, math.ceil(len(route_states) / total_stops))

    start_index = (stop_number - 1) * states_per_segment
    end_index = start_index + states_per_segment

    segment_states = route_states[start_index:end_index]

    if not segment_states:
        segment_states = [route_states[-1]]

    return segment_states


def calculate_fuel_plan(total_distance_miles, route_states):
    number_of_fuel_segments = math.ceil(total_distance_miles / MAX_RANGE_MILES)

    fuel_stops = []
    total_cost = 0
    remaining_distance = total_distance_miles

    used_station_ids = set()

    for stop_number in range(1, number_of_fuel_segments + 1):
        segment_states = get_states_for_segment(
            route_states,
            stop_number,
            number_of_fuel_segments
        )

        stations = FuelStation.objects.filter(
            state__in=segment_states
        ).order_by("retail_price")

        if not stations.exists():
            stations = FuelStation.objects.filter(
                state__in=route_states
            ).order_by("retail_price")

        if not stations.exists():
            stations = FuelStation.objects.order_by("retail_price")

        station = stations.exclude(id__in=used_station_ids).first() or stations.first()
        used_station_ids.add(station.id)

        miles_for_this_segment = min(MAX_RANGE_MILES, remaining_distance)
        gallons_needed = miles_for_this_segment / MILES_PER_GALLON
        cost = gallons_needed * station.retail_price

        fuel_stops.append({
            "stop_number": stop_number,
            "segment_states": segment_states,
            "station_name": station.truckstop_name,
            "address": station.address,
            "city": station.city.strip() if station.city else "",
            "state": station.state,
            "price_per_gallon": round(station.retail_price, 3),
            "miles_covered": round(miles_for_this_segment, 2),
            "gallons_needed": round(gallons_needed, 2),
            "cost": round(cost, 2)
        })

        total_cost += cost
        remaining_distance -= miles_for_this_segment

    return {
        "fuel_stops": fuel_stops,
        "total_fuel_cost": round(total_cost, 2),
        "fuel_efficiency_mpg": MILES_PER_GALLON,
        "max_range_miles": MAX_RANGE_MILES
    }