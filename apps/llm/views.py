from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from .llm import generate_conversation_response, get_trending_faqs
from .redis_cache import redis_client
from .utils import format_response_as_steps


class LLMConversationAPI(APIView):
    # Disable authentication completely for testing
    authentication_classes = []
    permission_classes = []  # Allow both authenticated and anonymous users

    def post(self, request):
        user_message = request.data.get("message")

        if not user_message:
            return Response({"error": "message is required"}, status=400)

        # For now, use a default identifier since auth is disabled
        # You can use IP address or session key as identifier
        user_id = request.META.get('REMOTE_ADDR', 'anonymous')

        chat_key = f"chat_history_{user_id}"

        # Added for testing
        # redis_client.delete(f"chat_history_{user_id}")

        conversation_data = redis_client.get(chat_key)
        conversation = eval(conversation_data) if conversation_data else []

        conversation.append({"role": "user", "content": user_message})
        conversation = conversation[-10:]

        assistant_response_raw = generate_conversation_response(conversation)

        assistant_response_steps = format_response_as_steps(
            assistant_response_raw)

        conversation.append(
            {"role": "assistant", "content": assistant_response_raw})

        redis_client.set(chat_key, str(conversation), ex=1800)

        return Response({
            "response": assistant_response_steps,
            "message_count": len(conversation)
        }, status=200)


class TrendingQuestionsAPI(APIView):
    # Disable authentication for testing
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        cache_key = "trending_questions"

        # Added for testing
        # redis_client.delete("trending_questions")

        # For now, use a default identifier since auth is disabled
        # You can use IP address or session key as identifier
        user_id = request.META.get('REMOTE_ADDR', 'anonymous')

        chat_key = f"chat_history_{user_id}"

        # Added for testing
        # redis_client.delete(f"chat_history_{user_id}")

        cached = redis_client.get(cache_key)
        if cached:
            return Response({
                "trending_questions": json.loads(cached),
                "cached": True
            }, status=200)

        trending = get_trending_faqs()
        redis_client.set(cache_key, json.dumps(trending), ex=43200)

        return Response({
            "trending_questions": trending,
            "cached": False
        }, status=200)
