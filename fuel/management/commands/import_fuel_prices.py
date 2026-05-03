import pandas as pd
from django.core.management.base import BaseCommand
from fuel.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel prices from CSV"

    def handle(self, *args, **kwargs):
        file_path = "data/fuel-prices-for-be-assessment.csv"

        df = pd.read_csv(file_path)

        FuelStation.objects.all().delete()

        stations = []

        for _, row in df.iterrows():
            stations.append(
                FuelStation(
                    opis_truckstop_id=row.get("OPIS Truckstop ID"),
                    truckstop_name=row.get("Truckstop Name"),
                    address=row.get("Address"),
                    city=row.get("City"),
                    state=row.get("State"),
                    rack_id=row.get("Rack ID"),
                    retail_price=row.get("Retail Price"),
                )
            )

        FuelStation.objects.bulk_create(stations)

        self.stdout.write(
            self.style.SUCCESS(f"Imported {len(stations)} fuel stations successfully")
        )