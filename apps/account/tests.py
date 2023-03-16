import logging

from django.test import TestCase
from django.urls import reverse

from apps.account.models import Account

logging.root.setLevel(logging.INFO)


class UserTestCase(TestCase):
    username = "test_user"
    password = "test"

    @classmethod
    def setUpTestData(cls):
        Account.objects.create_user(username=cls.username, password=cls.password, name="Test User")
        Account.objects.create_user(username=cls.username + "1", password=cls.password, name="Test User")
        Account.objects.create_user(username=cls.username + "2", password=cls.password, name="Test User")

    def test_signup(self):
        form_data = {
            "username": "test_user_1",
            "password": "abcd",
            "name": "Test User One"
        }
        response = self.client.post(reverse("account:list"), data=form_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Account.objects.filter(username="test_user_1").exists())

    def test_get_list(self):
        self.client.login(username=self.username, password=self.password)
        get_response = self.client.get(reverse("account:list"))
        self.assertEqual(get_response.status_code, 200)

    def test_get_specific_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("account:single", args=(self.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.username)

    def test_update_password(self):
        self.client.login(username=self.username, password=self.password)
        account = Account.objects.get(username=self.username)
        response = self.client.patch(reverse("account:single", args=(self.username,)), data={
            "password": "userABCD"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        account.refresh_from_db()
        self.assertTrue(account.check_password("userABCD"))

    def test_delete(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(reverse("account:single", args=(self.username,)))
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Account.objects.get(username=self.username).is_deleted)

    def test_following_list(self):
        self.client.login(username=self.username, password=self.password)
        account = Account.objects.get(username=self.username)
        account.follow.add(Account.objects.get(username=self.username + "1"))
        account.follow.add(Account.objects.get(username=self.username + "2"))
        response = self.client.get(reverse("account:following", args=(self.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_follower_list(self):
        self.client.login(username=self.username, password=self.password)
        account = Account.objects.get(username=self.username)
        account1 = Account.objects.get(username=self.username + "1")
        account1.follow.add(account)
        response = self.client.get(reverse("account:follower", args=(self.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_follower_create(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("account:following", args=(self.username,)), data={
            "follow_user": self.username + "1"
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("account:following", args=(self.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
