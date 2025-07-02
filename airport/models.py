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
