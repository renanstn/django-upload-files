from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status

from core import models


class TestAPI(APITestCase):
    def test_create_students_from_csv(self):
        """
        Test if the Students model is being correctly created from a CSV file
        """
        url = reverse("student-create-students-from-csv")

        with open(
            f"{settings.BASE_DIR}/core/tests/files/grades.csv", "rb"
        ) as file:
            payload = {"file": file}
            response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.Student.objects.filter(name="Aloysius Alfalfa").exists()
        )
        self.assertEqual(
            models.Student.objects.get(name="Aloysius Alfalfa").ssn,
            "123-45-6789",
        )
        self.assertEqual(models.Student.objects.count(), 16)
