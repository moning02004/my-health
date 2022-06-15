from datetime import datetime

from django.test import TestCase

from app_user.models import User, FollowUser


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
