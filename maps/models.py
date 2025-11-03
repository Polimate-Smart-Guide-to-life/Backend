from django.db import models

class Sede(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    latitude = models.FloatField(blank=True, null=True)     
    longitude = models.FloatField(blank=True, null=True)
    map_image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.name
    
    
class Campus(models.Model):
    sede = models.ForeignKey(
        Sede, on_delete=models.CASCADE, related_name="campuses",
        blank=True, null=True
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name="buildings")
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True, null=True)    
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    


    def __str__(self):
        return f"{self.name} ({self.campus.name})"
    
    
class Room(models.Model):  # "Aula"
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="rooms",   # accesso: building.rooms.all()
    )
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} — {self.building.name}"
