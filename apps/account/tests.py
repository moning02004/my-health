import logging

from django.test import TestCase

from apps.account.models import User

logging.root.setLevel(logging.INFO)


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User(username="test_user", name="Test User")
        self.user.set_password("test")
        self.user.save()
        self.user.refresh_from_db()

    def test_follow(self):
        user1 = User(username="user1@a.com", name="user1")
        user1.set_password("123")
        user1.save()

        user2 = User(username="user2@a.com", name="user2")
        user2.set_password("123")
        user2.save()

        user1.follow.add(user2)
        self.assertEqual(user1.following.all().count(), 1)  # 내가 Follow 하는 수
        self.assertEqual(user1.follower.all().count(), 0)  # 나를 Follow 하는 수

        user2.follow.add(user1)
        self.assertEqual(user1.follower.all().count(), 1)

    def test_signup(self):
        username = "test_user_1@a.com"
        form_data = {
            "username": username,
            "password": "abcd",
            "name": "Test User One"
        }
        response = self.client.post("/users", data=form_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_signup_failed(self):
        username = "test_user_1@a.com"
        form_data = {
            "username": username,
            "password": "abcd",
        }
        response = self.client.post("/users", data=form_data)
        self.assertEqual(response.status_code, 400)

    def test_get_list(self):
        username = "test_user_1@a.com"
        form_data = {
            "username": username,
            "password": "abcd",
            "name": "Test User One"
        }
        post_response = self.client.post("/users", data=form_data)
        self.assertEqual(post_response.status_code, 201)

        get_response = self.client.get("/users")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len([x for x in get_response.data if x["username"] == username]), 1)

    def test_get_specific_user(self):
        response = self.client.get(f"/users/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.user.id)

        response = self.client.get(f"/users/100")
        self.assertEqual(response.status_code, 404)

    def test_update_password(self):
        user_id = self.user.id
        new_password = "userABCD"
        data = {
            "password": new_password
        }
        response = self.client.patch(f"/users/{user_id}", data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("userABCD"))

    def test_delete(self):
        user_id = self.user.id
        response = self.client.delete(f"/users/{user_id}", content_type="application/json")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(pk=self.user.id).exists())

    def test_follow_list(self):
        user_id = self.user.id
        friends = ["friend1", "friend2", "follower1"]
        for test_text in friends:
            friend = User(username=test_text, name=test_text)
            friend.set_password(test_text)
            friend.save()

            if test_text.startswith("follower"):
                friend.follow.add(self.user)
            self.user.follow.add(friend)
        self.client.login(username="test_user", password="test")
        response = self.client.get(f"/users/{user_id}/followers")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data["follower"]), 1)
        self.assertEqual(len(response.data["following"]), len(friends))

    def test_request_follow(self):
        follow_user = User(username="follow_user1", name="follow_user1")
        follow_user.set_password("follow_user1")
        follow_user.save()
        self.client.login(username="test_user", password="test")
        response = self.client.post(f"/users/{follow_user.id}/follow")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user.following.count(), 1)
        self.assertEqual(self.user.follower.count(), 0)

    def test_request_unfollow(self):
        follow_user = User(username="follow_user1", name="follow_user1")
        follow_user.set_password("follow_user1")
        follow_user.save()
        self.client.login(username="test_user", password="test")
        self.user.follow.add(follow_user)
        self.assertEqual(self.user.following.count(), 1)

        response = self.client.put(f"/users/{follow_user.id}/unfollow")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.following.count(), 0)
