from rest_framework import serializers
from .models import Sede, Campus, Building, Room

class RoomForMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name")

class BuildingForMapSerializer(serializers.ModelSerializer):
    rooms = RoomForMapSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = (
            "id", "name", "code", "address",
            "latitude", "longitude",
            "opening_hours",
            "rooms",
        )

class CampusMapSerializer(serializers.ModelSerializer):
    sede = serializers.SerializerMethodField()
    buildings = BuildingForMapSerializer(many=True, read_only=True)

    class Meta:
        model = Campus
        fields = (
            "id", "name", "slug",
            "latitude", "longitude",
            "sede",
            "buildings",
        )

    def get_sede(self, obj):
        if obj.sede:
            return {
                "id": obj.sede.id,
                "name": obj.sede.name,
                "slug": obj.sede.slug,
                "latitude": obj.sede.latitude,
                "longitude": obj.sede.longitude,
                "map_image_url": obj.sede.map_image_url,
            }
        return None

class RoomDetailSerializer(serializers.ModelSerializer):
    building = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "name", "building")

    def get_building(self, obj):
        b = obj.building
        return {
            "id": b.id,
            "name": b.name,
            "code": b.code,
            "address": b.address,
            "latitude": b.latitude,
            "longitude": b.longitude,
        }