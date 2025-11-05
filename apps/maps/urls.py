from django.urls import path
from .views import CampusMapView, BuildingDetailView, RoomDetailView

urlpatterns = [
    path("maps/<slug:slug>/", CampusMapView.as_view(), name="campus-map"),
    path("buildings/<int:pk>/", BuildingDetailView.as_view(), name="building-detail"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),

]
