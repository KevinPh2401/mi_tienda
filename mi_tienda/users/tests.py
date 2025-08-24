from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="kevin", password="123456", phone="123456789", address="Barranquilla")
        self.assertEqual(user.username, "kevin")
        self.assertEqual(user.phone, "123456789")
        self.assertEqual(user.address, "Barranquilla")
        self.assertTrue(user.check_password("123456"))
