from django.db import models

# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"Airport: {self.name}, closest_big_city: {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE)
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE)
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
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: {self.name}, Airplane Type: {self.airplane_type}, rows: {self.rows}, seats_in_row: {self.seats_in_row}"

