from django.db import models
from rest_framework.exceptions import ValidationError

from airport_api import settings


# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"Airport: {self.name}, closest_big_city: {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="sources")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="destinations")
    distance = models.IntegerField()

    def __str__(self):
        return f"Route: {self.source}, {self.destination}, distance: {self.distance}"


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Crew: {self.first_name}, {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Airplane Type: {self.name}"


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplanes")

    def __str__(self):
        return f"Name: {self.name}, Airplane Type: {self.airplane_type}, rows: {self.rows}, seats_in_row: {self.seats_in_row}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order created at: {self.created_at}, user: {self.user}"


class Flight(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, related_name="flights")
    crew = models.ManyToManyField("Crew", related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        crew_names = ", ".join(str(member) for member in self.crew.all())
        return f"Route: {self.route}, airplane: {self.airplane}, crew: {crew_names}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    def clean(self):
        if not 1 <= self.row <= self.flight.airplane.rows:
            raise ValidationError(f"Row must be in range of {self.flight.airplane.rows}, not {self.row}")
        if not 1 <= self.seat <= self.flight.airplane.seats_in_row:
            raise ValidationError(f"Seats must be in range of {self.flight.airplane.seats_in_row}, not {self.seat}")

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ("row", "seat", "flight")
        ordering = ["row", "seat"]

    def __str__(self):
        return f"Row: {self.row}, seat: {self.seat}, flight: {self.flight}, order: {self.order}"



