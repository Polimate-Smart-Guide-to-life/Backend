# maps/views.py
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import BuildingForMapSerializer
from .models import Campus, Building, Room
from .serializers import CampusMapSerializer

from .serializers import RoomDetailSerializer


class CampusMapView(APIView):
    """
    UNICO ENDPOINT:
    GET /api/maps/<slug:slug>/
    Ritorna sempre: campus + buildings + rooms
    """
    authentication_classes = []   # pubblico
    permission_classes = []

    def get(self, request, slug):
        # Prefetch rooms dentro i buildings per evitare N+1 query
        rooms_qs = Room.objects.only("id", "name", "building_id").order_by("name")
        buildings_qs = (
            Building.objects
            .only("id", "name", "code", "address", "latitude", "longitude", "opening_hours", "campus_id")
            .filter(campus__slug=slug)
            .order_by("name")
            .prefetch_related(Prefetch("rooms", queryset=rooms_qs))
        )

        try:
            campus = (
                Campus.objects
                .select_related("sede")
                .only("id", "name", "slug", "latitude", "longitude", "sede_id")
                .prefetch_related(Prefetch("buildings", queryset=buildings_qs))
                .get(slug=slug)
            )
        except Campus.DoesNotExist:
            raise NotFound(detail=f"Campus con slug '{slug}' non trovato.")

        return Response(CampusMapSerializer(campus).data)
    
    
class BuildingDetailView(APIView):
    """
    GET /api/buildings/<int:pk>/
    Ritorna: edificio + rooms
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        rooms_qs = Room.objects.only("id", "name", "building_id").order_by("name")
        try:
            building = (
                Building.objects
                .only("id", "name", "code", "address", "latitude", "longitude", "opening_hours", "campus_id")
                .prefetch_related(Prefetch("rooms", queryset=rooms_qs))
                .get(pk=pk)
            )
        except Building.DoesNotExist:
            raise NotFound(detail=f"Building con id '{pk}' non trovato.")

        return Response(BuildingForMapSerializer(building).data)


class RoomDetailView(APIView):
    """
    GET /api/rooms/<int:pk>/
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        try:
            room = (
                Room.objects
                .select_related("building")
                .only("id", "name", "building__id", "building__name",
                      "building__code", "building__address",
                      "building__latitude", "building__longitude")
                .get(pk=pk)
            )
        except Room.DoesNotExist:
            raise NotFound(detail=f"Room con id '{pk}' non trovata.")

        return Response(RoomDetailSerializer(room).data)