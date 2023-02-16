from rest_framework.test import APITestCase

from apps.account.models import User
from apps.workout.models import Part, Workout


class WorkoutTestCase(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="test")
        user.set_password("test")
        user.save()
        part1 = Part.objects.get(name="등")
        part2 = Part.objects.get(name="가슴")
        part3 = Part.objects.get(name="팔")

        self.workout1 = Workout.objects.create(name="랫풀 다운", description="등 운동입니다.", status="PUB")
        self.workout1.effective_part.add(part1)
        self.workout1.effective_part.add(part3)

        workout2 = Workout.objects.create(name="벤치프레스", description="가슴 운동입니다.", status="PUB")
        workout2.effective_part.add(part2)
        self.client.login(username="test", password="test")

    def test_list(self):
        response = self.client.get("/workout", data={
            "part": "등"
        })
        self.assertEqual(response.status_code, 200)

    def test_list_all(self):
        response = self.client.get("/workout")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post("/workout", data={
            "name": "Seated Row",
            "description": "등 운동입니다.",
            "part_id": [1, 3]
        })
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/workout")
        self.assertEqual(response.status_code, 200)

    def test_detail_workout(self):
        response = self.client.get(f"/workout/{self.workout1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["effective_part"]), 2)

    def test_partial_update_workout(self):
        test_text = "등 운동이며 협응근은 이두입니다."
        response = self.client.patch(f"/workout/{self.workout1.id}", data={
            "description": test_text
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], test_text)
