from django.test import TestCase

from app_user.models import User
from app_workout.models import Part


class WorkoutTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="test")
        user.set_password("test")
        user.save()
        self.client.login(username="test", password="test")

    def test_list(self):
        response = self.client.get("/workout")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        Part.objects.create(name="등")
        response = self.client.post("/workout", data={
            "name": "Seated Row",
            "description": "등 운동입니다.",
            "part_id": 1
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/workout")
        print(response.data)

