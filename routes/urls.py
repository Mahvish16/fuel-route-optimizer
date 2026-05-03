from django.urls import path
from .views import FuelPlanAPIView

urlpatterns = [
    path("fuel-plan/", FuelPlanAPIView.as_view(), name="fuel-plan"),
]