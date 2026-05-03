from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import FuelPlanRequestSerializer
from .services.routing_service import get_route
from .services.fuel_optimizer import calculate_fuel_plan


class FuelPlanAPIView(APIView):
    def post(self, request):
        serializer = FuelPlanRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_location = serializer.validated_data["start_location"]
        finish_location = serializer.validated_data["finish_location"]

        try:
            route = get_route(start_location, finish_location)

            route_states = route.get("route_states", [])

            fuel_plan = calculate_fuel_plan(
                route["distance_miles"],
                route_states
            )

            return Response({
                "start_location": start_location,
                "finish_location": finish_location,
                "route_states": route_states,
                "total_distance_miles": round(route["distance_miles"], 2),
                "duration_minutes": round(route["duration_minutes"], 2),
                "max_range_miles": fuel_plan["max_range_miles"],
                "fuel_efficiency_mpg": fuel_plan["fuel_efficiency_mpg"],
                "fuel_stops": fuel_plan["fuel_stops"],
                "total_fuel_cost": fuel_plan["total_fuel_cost"],
                "route_map_geojson": route["geometry"],
                "start_coordinates": route["start_coordinates"],
                "finish_coordinates": route["finish_coordinates"]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)