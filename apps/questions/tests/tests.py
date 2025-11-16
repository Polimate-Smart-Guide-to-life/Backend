import time
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.questions.models import Question

_help_support_start = None

class CreateQuestionAPITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global _help_support_start
        _help_support_start = time.time()
        print("\n" + "="*60)
        print("Running Help & Support Tests....")
        print("="*60)

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword123"
        )
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse('create-question')

    def test_create_question(self):
        print("\nQUESTION TEST 1: Creating a new question")
        data = {
            "text": "How do I reset my password?",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["text"], "How do I reset my password?")
        self.assertEqual(response.data["user"], (self.user.id))
        print("\nQUESTION TEST 1: PASSED ✓")


class GetUserQuestionsAPITestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        try:
            elapsed = None
            if globals().get("_help_support_start") is not None:
                elapsed = time.time() - globals()["_help_support_start"]
            print("\n" + "="*60)
            print("All Help & Support tests completed successfully!")
            if elapsed is not None:
                print(f"Total execution time: {elapsed:.2f} seconds")
            print("="*60 + "\n")
        finally:
            super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword123"
        )
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse('user-questions')

        Question.objects.create(
            user=self.user,
            text="How do I reset my password?"
        )
        Question.objects.create(
            user=self.user,
            text="How do we reset our passwords?"
        )

    def test_get_user_questions(self):
        print("\nQUESTION TEST 2: Retrieving user questions")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0]["text"],
            "How do I reset my password?"
            )
        self.assertEqual(
            response.data[1]["text"],
            "How do we reset our passwords?"
            )
        print("\nQUESTION TEST 2: PASSED ✓")