from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport import views

router = DefaultRouter()
router.register("airports", views.AirportViewSet)
router.register("routes", views.RouteViewSet)
router.register("crews", views.CrewViewSet)
router.register("airplanes", views.AirplaneViewSet)
router.register("airplane_types", views.AirplaneTypeViewSet)
router.register("orders", views.OrderViewSet)
router.register("tickets", views.TicketViewSet)
router.register("flights", views.FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]