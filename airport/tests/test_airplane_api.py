from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import AirplaneType, Airplane
from airport.serializers import AirplaneListSerializer, AirplaneRetrieveSerializer

AIRPLANE_URL = reverse("airport:airplane-list")


def sample_airplane(**params):
    airplane_type = AirplaneType.objects.create(name="test")

    defaults = {
        "name": "sample airplane",
        "rows": 20,
        "seats_in_row": 20,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def image_upload_url(airplane_id):
    """Return URL for recipe image upload"""
    return reverse("airport:airplane-upload-image", args=[airplane_id])


def detail_url(movie_id):
    return reverse("airport:airplane-detail", args=[movie_id])


class UnauthenticatedAirplaneTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane(self):
        sample_airplane()
        sample_airplane()

        res = self.client.get(AIRPLANE_URL)

        airplanes = Airplane.objects.order_by("id")
        serializer = AirplaneListSerializer(airplanes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_movies_by_airplane_type(self):
        airplane_type1 = AirplaneType.objects.create(name="name1")
        airplane_type2 = AirplaneType.objects.create(name="name2")

        airplane1 = sample_airplane(name="air1", airplane_type=airplane_type1)
        airplane2 = sample_airplane(name="air2", airplane_type=airplane_type2)

        res = self.client.get(
            AIRPLANE_URL, {"airplane_types": f"{airplane_type1.id},{airplane_type2.id}"}
        )

        serializer1 = AirplaneListSerializer(airplane1)
        serializer2 = AirplaneListSerializer(airplane2)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_retrieve_airplanes_detail(self):
        airplane = sample_airplane()

        url = detail_url(airplane.id)
        res = self.client.get(url)

        serializer = AirplaneRetrieveSerializer(airplane)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_forbidden(self):
        payload = {
            "name": "test",
            "rows": 20,
            "seats_in_row": 20,
            "airplane_type": AirplaneType.objects.create(name="test"),
        }
        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = AirplaneType.objects.create(name="test")

        payload = {
            "name": "test",
            "rows": 20,
            "seats_in_row": 20,
            "airplane_type": airplane_type.id,
        }
        res = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.get(id=res.data["id"])

        self.assertEqual(payload["name"], airplane.name)
        self.assertEqual(payload["rows"], airplane.rows)
        self.assertEqual(payload["seats_in_row"], airplane.seats_in_row)
        self.assertEqual(payload["airplane_type"], airplane.airplane_type.id)
