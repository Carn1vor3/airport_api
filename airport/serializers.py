from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from airport.models import Airport, Route, Crew, AirplaneType, Airplane, Order, Flight, Ticket


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteRetrieveSerializer(serializers.ModelSerializer):
    source = AirportSerializer()
    destination = AirportSerializer()
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class CrewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "full_name")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type", "capacity")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(read_only=True, slug_field="name")


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer()
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type", "capacity")


class AirplaneTypeRetrieveSerializer(serializers.ModelSerializer):
    airplanes = AirplaneSerializer(many=True)
    class Meta:
        model = AirplaneType
        fields = ("id", "name", "airplanes")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")

    def get_route(self, obj):
        return f"{obj.route.source.name} → {obj.route.destination.name}"


class FlightListSerializer(FlightSerializer):
    airplane = serializers.SlugRelatedField(read_only=True, slug_field="name")
    crew = serializers.SlugRelatedField(read_only=True, slug_field="full_name", many=True)
    route = serializers.SerializerMethodField()


class FlightRetrieveSerializer(FlightSerializer):
    airplane = AirplaneRetrieveSerializer()
    crew = CrewSerializer(many=True)
    route = RouteRetrieveSerializer()


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class TicketRetrieveSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True,read_only=False, allow_empty=False)
    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                ticket = Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketShortSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")


class OrderRetrieveSerializer(serializers.ModelSerializer):
    tickets = TicketRetrieveSerializer(many=True)
    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")
