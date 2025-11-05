from django.core.management.base import BaseCommand
from django.db.models import Avg
from maps.models import Campus, Building

class Command(BaseCommand):
    help = "Calcola e aggiorna latitude/longitude per ogni campus in base ai suoi edifici"

    def handle(self, *args, **options):
        updated = 0
        for campus in Campus.objects.all():
            avg = Building.objects.filter(campus=campus).aggregate(
                lat=Avg("latitude"),
                lon=Avg("longitude"),
            )
            if avg["lat"] is not None and avg["lon"] is not None:
                campus.latitude = avg["lat"]
                campus.longitude = avg["lon"]
                campus.save(update_fields=["latitude", "longitude"])
                self.stdout.write(self.style.SUCCESS(
                    f"✅ {campus.name}: aggiornato a ({avg['lat']:.5f}, {avg['lon']:.5f})"
                ))
                updated += 1
            else:
                self.stdout.write(self.style.WARNING(
                    f"⚠️ {campus.name}: nessun edificio con coordinate, saltato"
                ))
        self.stdout.write(self.style.SUCCESS(f"Totale campus aggiornati: {updated}"))
