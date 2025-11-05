import csv
from django.core.management.base import BaseCommand
from maps.models import Campus, Building

def norm(s: str) -> str:
    """Normalizza stringhe: rimuove BOM, spazi, va in minuscolo per header."""
    return (s or "").replace("\ufeff", "").strip()

def to_float_or_none(v: str):
    """Converte stringhe in float (gestisce virgola decimale). Vuoto -> None."""
    if v is None:
        return None
    v = str(v).strip()
    if not v:
        return None
    v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None

class Command(BaseCommand):
    help = "Import buildings from CSV (robusto: delimiter sniff, header norm, lat/lon parsing)"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Percorso del file CSV")

    def handle(self, *args, **opts):
        path = opts["csv_file"]

        # 1) Leggi un sample per riconoscere il delimitatore
        with open(path, "r", encoding="utf-8", newline="") as f:
            sample = f.read(4096)
            f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"])
            except csv.Error:
                # fallback semplice tra ; e ,
                dialect = csv.excel
                dialect.delimiter = ";" if sample.count(";") > sample.count(",") else ","

            # leggi header raw per log
            reader = csv.reader(f, dialect)
            raw_headers = next(reader)
            headers = [norm(h).lower() for h in raw_headers]

        self.stdout.write(self.style.WARNING(f"Intestazioni rilevate: {headers}"))

        # 2) Riapri come DictReader con lo stesso dialect e header normalizzati
        created = updated = skipped = 0
        with open(path, "r", encoding="utf-8", newline="") as f:
            dr = csv.DictReader(f, dialect=dialect)
            # normalizza i nomi colonna del DictReader
            dr.fieldnames = [norm(h).lower() for h in (dr.fieldnames or [])]

            # utility per prendere il primo valore disponibile tra più chiavi alternative
            def getv(row, *keys):
                for k in keys:
                    if k in row and row[k] is not None:
                        v = str(row[k]).strip()
                        if v != "":
                            return v
                return ""

            for i, row in enumerate(dr, start=2):  # parte dalla riga dopo l'header
                # normalizza chiavi riga (alcune versioni di DictReader non riassegnano)
                row = {norm(k).lower(): (v if v is not None else "") for k, v in row.items()}

                slug = getv(row, "campus_slug", "slug")
                code = getv(row, "code")
                name = getv(row, "name")
                address = getv(row, "address")  # ora salviamo in address

                lat = to_float_or_none(getv(row, "latitude"))
                lng = to_float_or_none(getv(row, "longitude"))

                if not slug or not code or not name:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(
                        f"Riga {i}: campi mancanti (slug/campus_slug, code, name) → salto"
                    ))
                    continue

                try:
                    campus = Campus.objects.get(slug=slug)
                except Campus.DoesNotExist:
                    skipped += 1
                    self.stdout.write(self.style.ERROR(
                        f"Riga {i}: Campus non trovato: {slug} → salto"
                    ))
                    continue

                # update_or_create su (campus, code)
                obj, is_created = Building.objects.update_or_create(
                    campus=campus,
                    code=str(code),
                    defaults={
                        "name": name,
                        "address": address,   # <— salva nel campo address del modello
                        "latitude": lat,
                        "longitude": lng,
                    }
                )

                if is_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import completato! Creati: {created}, Aggiornati: {updated}, Saltati: {skipped}"
        ))
