from django.test import TestCase

from app_user.models import User


class UserTestCase(TestCase):
    def test_follow(self):
        user1 = User(username="user1@a.com", name="user1")
        user1.set_password("123")
        user1.save()

        user2 = User(username="user2@a.com", name="user2")
        user2.set_password("123")
        user2.save()

        user1.follow.add(user2)
        self.assertEqual(user1.following.all().count(), 1)  # 나를 Follow 하는 수
        self.assertEqual(user1.follower.all().count(), 0)  # 내가 Follow 하는 수

        user2.follow.add(user1)
        self.assertEqual(user1.follower.all().count(), 1)

    def test_signup_user(self):
        username = "test_user_1@a.com"
        form_data = {
            "username": username,
            "password1": "abcd",
            "password2": "abcd",
            "name": "Test User One"
        }
        response = self.client.post("/users", data=form_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_get_users(self):
        username = "test_user_1@a.com"
        form_data = {
            "username": username,
            "password1": "abcd",
            "password2": "abcd",
            "name": "Test User One"
        }
        post_response = self.client.post("/users", data=form_data)
        self.assertEqual(post_response.status_code, 201)

        get_response = self.client.get("/users")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len([x for x in get_response.data if x["username"] == username]), 1)
