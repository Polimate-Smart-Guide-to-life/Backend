import csv
from django.core.management.base import BaseCommand
from maps.models import Building, Room

class Command(BaseCommand):
    help = "Import rooms from CSV (usa building_code invece di building_id)"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Percorso del file CSV")

    def handle(self, *args, **opts):
        path = opts["csv_file"]

        created = updated = skipped = 0
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for i, row in enumerate(reader, start=2):
                code = (row.get("building_code") or "").strip()
                name = (row.get("room_name") or "").strip()

                if not code or not name:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"Riga {i}: campi mancanti"))
                    continue

                try:
                    building = Building.objects.get(code=code)
                except Building.DoesNotExist:
                    skipped += 1
                    self.stdout.write(self.style.ERROR(
                        f"Riga {i}: edificio con code={code} non trovato"
                    ))
                    continue

                obj, created_flag = Room.objects.update_or_create(
                    building=building,
                    name=name
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import completato! Creati: {created}, Aggiornati: {updated}, Saltati: {skipped}"
        ))
