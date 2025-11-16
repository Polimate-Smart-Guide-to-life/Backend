import time
from rest_framework.test import APITestCase
from django.urls import reverse

from apps.users.factories import UserFactory

class CreateUserTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.start_time = time.time()
        print("\n" + "="*60)
        print("Running User Tests....")
        print("="*60)
    
    @classmethod
    def tearDownClass(cls):
        elapsed_time = time.time() - cls.start_time
        print("\n" + "="*60)
        print("All user tests completed successfully!")
        print(f"Total execution time: {elapsed_time:.2f} seconds")
        print("="*60 + "\n")
        super().tearDownClass()

    def setUp(self) -> None:
        self.user = UserFactory(username="test")
        self.user.set_password("test")
        self.user.save()

    def test_create_user(self):
        print("\nUSER TEST 1: Creating a new user")
        url = reverse("users-register")
        data = {
            "username": "test1",
            "first_name": "Test",
            "middle_name": "test",
            "last_name": "Test",
            "email": "test1@gmail.com",
            "enrollment_number": "10676352",
            "password": "Hello1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], "test1")
        print("\nUSER TEST 1: PASSED ✓")

    def test_get_me(self):
        print("\nUSER TEST 2: Getting user details")
        url = reverse("users-me")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["enrollment_number"], self.user.enrollment_number)
        print("\nUSER TEST 2: PASSED ✓")

    def test_login(self):
        print("\nUSER TEST 3: Logging in")
        url = reverse("token_obtain_pair")
        data = {
            "username": "test",
            "password": "test"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        print("\nUSER TEST 3: PASSED ✓")

    def test_update_me(self):
        print("\nUSER TEST 4: Updating user details")
        url = reverse("users-me")
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"first_name": "New Name"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "New Name")
        print("\nUSER TEST 4: PASSED ✓")