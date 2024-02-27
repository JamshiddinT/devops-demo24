from django.test import TestCase
from django.contrib.auth.models import User


class UsersTestCase(TestCase):
    def setUp(self):
        self.admin_username = "admin"
        self.admin_password = "adminpass"
        self.test_username = "test"
        self.test_password = "testpass"

        self.admin_user = User.objects.create_superuser(
            username=self.admin_username, password=self.admin_password
        )

        self.user = User.objects.create_user(
            username=self.test_username, password=self.test_password
        )

    def test_user_login(self):
        login = self.client.login(
            username=self.admin_username, password=self.admin_password
        )
        self.assertEqual(login, True, msg="Could not login with correct credentials")

        login = self.client.login(username=self.admin_username, password="incorrect")
        self.assertEqual(login, False, msg="Logged in with incorrect credentials")
        self.client.logout()

    def test_get_users_list_as_admin(self):
        self.client.login(username=self.admin_username, password=self.admin_password)
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.client.logout()

    def test_get_users_list_as_user(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_get_users_list_as_unauth_user(self):
        self.client.logout()
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 403)
