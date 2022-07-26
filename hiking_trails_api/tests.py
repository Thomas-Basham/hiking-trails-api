from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import HikingTrails

import fire
import requests

# NOTE: Adjust these settings as needed
API_HOST = "http://localhost:8000"
RESOURCE_URI = "hiking-trails-api"
USERNAME = "admin"
PASSWORD = "admin"

class HikingTrailsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="awefoijawef"
        )
        testuser1.save()

        test_hiking_trail = HikingTrails.objects.create(
            owner=testuser1,
            wta_link="https://www.wta.org/go-hiking/hikes/spectacle-lake",
            description="This is a great trail for testing purposes",
        )
        test_hiking_trail.save()

        
    def test_hiking_trails_model(self):
        hiking_trail = HikingTrails.objects.get(id=1)
        actual_owner = str(hiking_trail.owner)
        actual_name = str(hiking_trail.trail_name)
        actual_lat = str(hiking_trail.lat)
        actual_lon = str(hiking_trail.lon)
        actual_description = str(hiking_trail.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "Spectacle Lake")
        self.assertEqual(actual_lat, "47.4337")
        self.assertEqual(actual_lon, "-121.1888")
        self.assertEqual(
            actual_description, "This is a great trail for testing purposes"
        )

    def test_get_hiking_trail_list(self):
        url = reverse("hiking_trails_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hiking_trails = response.data
        self.assertEqual(len(hiking_trails), 1)
        self.assertEqual(hiking_trails[0]["trail_name"], "Spectacle Lake")

    def test_get_hiking_trail_by_id(self):
        url = reverse("hiking_trails_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hiking_trail = response.data
        self.assertEqual(hiking_trail["trail_name"], "Spectacle Lake")

    def test_create_hiking_trail(self):
        url = reverse("hiking_trails_list")
        data = {"owner": 1, "wta_link": "https://www.wta.org/go-hiking/hikes/clear-lake-interpretive-trail", "description": "Another Great trail for testing"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hiking_trails = HikingTrails.objects.all()
        self.assertEqual(len(hiking_trails), 2)
        self.assertEqual(HikingTrails.objects.get(id=2).trail_name, "Clear Lake Interpretive Trail")

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("hiking_trails_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse("hiking_trails_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def setUp(self):
        self.client.login(username="testuser1", password="awefoijawef")

    def test_update_hiking_trail(self):
        url = reverse("hiking_trails_detail", args=(1,))
        data = {
            "owner": 1,
            "trail_name": "Spectacle Lake",
            "description": "Updating this lake",
            "google_maps_directions": "Updating this lake",
            "wta_link": "https://www.wta.org/go-hiking/hikes/spectacle-lake",
            "lat": "123",
            "lon": "456",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hiking_trail = HikingTrails.objects.get(id=1)
        self.assertEqual(hiking_trail.trail_name, data["trail_name"])
        self.assertEqual(hiking_trail.owner.id, data["owner"])
        self.assertEqual(hiking_trail.description, data["description"])

    def test_delete_hiking_trail(self):
        url = reverse("hiking_trails_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        hiking_trails = HikingTrails.objects.all()
        self.assertEqual(len(hiking_trails), 0)

