from django.urls import path
from .views import RouteFuelAPIView

urlpatterns = [
    path("route/", RouteFuelAPIView.as_view(), name="route-fuel"),
]