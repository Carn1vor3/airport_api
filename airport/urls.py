from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport import views
from airport_api import settings

router = DefaultRouter()
router.register("airports", views.AirportViewSet)
router.register("routes", views.RouteViewSet)
router.register("crews", views.CrewViewSet)
router.register("airplanes", views.AirplaneViewSet)
router.register("airplane_types", views.AirplaneTypeViewSet)
router.register("orders", views.OrderViewSet)
router.register("flights", views.FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
