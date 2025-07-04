from django.db.models import Count, F
from django.shortcuts import render
from rest_framework import viewsets

from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Order,
    Ticket,
    Flight,
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    OrderSerializer,
    TicketSerializer,
    FlightSerializer,
    RouteRetrieveSerializer,
    RouteListSerializer,
    CrewListSerializer,
    AirplaneTypeRetrieveSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    TicketRetrieveSerializer,
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if source:
            source_ids = [int(source_id) for source_id in source.split(",")]
            self.queryset = self.queryset.filter(source__id__in=source_ids)
        if destination:
            destination_ids = [int(dest_id) for dest_id in destination.split(",")]
            self.queryset = self.queryset.filter(destination__id__in=destination_ids)

        if self.action in ("list", "retrieve"):
            return self.queryset.select_related("source", "destination")
        else:
            return self.queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        elif self.action == "list":
            return RouteListSerializer
        else:
            return RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer
        else:
            return CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.prefetch_related("airplanes")
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirplaneTypeRetrieveSerializer
        else:
            return AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()

    def get_queryset(self):
        airplane_type = self.request.query_params.get("airplane_type")
        if airplane_type:
            airplane_type_ids = [int(str_id) for str_id in airplane_type.split(",")]
            self.queryset = self.queryset.filter(
                airplane_type__id__in=airplane_type_ids
            )

        if self.action in ("list", "retrieve"):
            return self.queryset.select_related("airplane_type")
        else:
            return self.queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        elif self.action == "retrieve":
            return AirplaneRetrieveSerializer
        else:
            return AirplaneSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(user=self.request.user).prefetch_related("tickets")
        if self.action == "retrieve":
            return queryset.filter(user=self.request.user).prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__flight__airplane__airplane_type",
                "tickets__flight__crew",
            )
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        else:
            return OrderSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()

    def get_queryset(self):
        crew = self.request.query_params.get("crew")
        route = self.request.query_params.get("route")

        if crew:
            crew_ids = [int(crew_id) for crew_id in crew.split(",")]
            self.queryset = self.queryset.filter(crew__id__in=crew_ids)

        if route:
            route_ids = [int(route_id) for route_id in route.split(",")]
            self.queryset = self.queryset.filter(route__id__in=route_ids)

        if self.action == "list":
            return self.queryset.select_related(
                "airplane__airplane_type", "route__source", "route__destination"
            ).prefetch_related("crew")
        elif self.action == "retrieve":
            return (
                self.queryset.select_related(
                    "airplane__airplane_type", "route__source", "route__destination"
                )
                .prefetch_related("crew")
                .annotate(
                    tickets_available=(
                        F("airplane__rows") * F("airplane__seats_in_row")
                    )
                    - Count("tickets")
                )
            )

        return self.queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightRetrieveSerializer
        else:
            return FlightSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return self.queryset.select_related(
                "order",
                "flight__airplane__airplane_type",
                "flight__route__source",
                "flight__route__destination",
            ).prefetch_related("flight__crew")
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TicketRetrieveSerializer
        else:
            return TicketSerializer
