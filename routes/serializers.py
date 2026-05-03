from rest_framework import serializers


class FuelPlanRequestSerializer(serializers.Serializer):
    start_location = serializers.CharField()
    finish_location = serializers.CharField()