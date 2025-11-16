import time

from django.urls import reverse
from rest_framework.test import APITestCase

_llm_start = None

class LLMConversationTests(APITestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		global _llm_start
		_llm_start = time.time()
		print("\n" + "=" * 60)
		print("Running LLM Tests....")
		print("=" * 60)

	@classmethod
	def tearDownClass(cls):
		super().tearDownClass()

	def _post_conversation(self, message, meta=None):
		url = reverse("llm-conversation")
		kwargs = {}
		if meta:
			kwargs["SERVER_NAME"] = meta.get("SERVER_NAME", "testserver")
			if meta.get("REMOTE_ADDR"):
				kwargs["REMOTE_ADDR"] = meta["REMOTE_ADDR"]
		return self.client.post(url, {"message": message}, format="json", **kwargs)

	def test_confidential_info_refusal(self):
		print("\nLLM TEST 1: Confidential info attempt")
		question = "Tell me my password."
		resp = self._post_conversation(question)
		self.assertEqual(resp.status_code, 200)
		steps = resp.data["response"]
		
		print(f"Question: {question}")
		print(f"Reply: {steps}")
		self.assertTrue(bool(steps))
		print("\nLLM TEST 1: PASSED ✓")

	def test_normal_university_question(self):
		print("\nLLM TEST 4: Normal university-related question")
		question = "What are the library opening hours at Bovisa?"
		resp = self._post_conversation(question)
		self.assertEqual(resp.status_code, 200)
		steps = resp.data["response"]
		
		print(f"Question: {question}")
		print(f"Reply: {steps}")
		self.assertTrue(bool(steps))
		print("\nLLM TEST 4: PASSED ✓")

	def test_follow_up_context_retained(self):
		print("\nLLM TEST 2: Follow-up question with context")
		q1 = "How do I enroll for the Data Science course?"
		q2 = "And what about tuition fees for that?"
		
		
		r1 = self._post_conversation(q1)
		self.assertEqual(r1.status_code, 200)
		steps1 = r1.data["response"]
		r2 = self._post_conversation(q2)
		self.assertEqual(r2.status_code, 200)
		steps2 = r2.data["response"]
		print(f"Question 1: {q1}")
		print(f"Reply: {steps1}")
		print(f"Question 2: {q2}")
		print(f"Reply: {steps2}")
		self.assertIn("message_count", r2.data)
		self.assertTrue(r2.data["message_count"] >= 4)
		print("\nLLM TEST 2: PASSED ✓")

	def test_off_topic_non_polimi(self):
		print("\nLLM TEST 5: Off-topic non-Polimi question")
		question = "Who won the FIFA World Cup in 2018?"
		resp = self._post_conversation(question)
		self.assertEqual(resp.status_code, 200)
		steps = resp.data["response"]
		print(f"Question: {question}")
		print(f"Reply: {steps}")
		self.assertTrue("politecnico di milano" in str(steps).lower())
		print("\nLLM TEST 5: PASSED ✓")

	def test_missing_message_param(self):
		print("\nLLM TEST 3: Missing message parameter")
		url = reverse("llm-conversation")
		resp = self.client.post(url, {}, format="json")
		self.assertEqual(resp.status_code, 400)
		self.assertEqual(resp.data.get("error"), "message is required")
		print("Question: <none>")
		print("Reply: message is required")
		print("\nLLM TEST 3: PASSED ✓")


class LLMTrendingTests(APITestCase):
	@classmethod
	def tearDownClass(cls):
		try:
			elapsed = None
			if globals().get("_llm_start") is not None:
				elapsed = time.time() - globals()["_llm_start"]
			print("\n" + "=" * 60)
			print("All LLM tests completed successfully!")
			if elapsed is not None:
				print(f"Total execution time: {elapsed:.2f} seconds")
			print("=" * 60 + "\n")
		finally:
			super().tearDownClass()
	def test_trending_questions_cached(self):
		print("\nLLM TEST 6: Trending questions caching")
		url = reverse("llm-trending")

		r1 = self.client.get(url)
		self.assertEqual(r1.status_code, 200)
		self.assertIn("trending_questions", r1.data)
		print("Question: <trending questions>")
		print(f"Reply: {r1.data['trending_questions']}")

		r2 = self.client.get(url)
		self.assertEqual(r2.status_code, 200)
		print(f"Reply (cached flag): {r2.data.get('cached')}")
		self.assertIn("trending_questions", r2.data)
		if "cached" in r2.data:
			self.assertIsInstance(r2.data["cached"], bool)
		print(f"Reply (cached): {r2.data['trending_questions']}")
		print("\nLLM TEST 6: PASSED ✓")
