from django.urls import path
from .views import LLMConversationAPI, TrendingQuestionsAPI

urlpatterns = [
    path('llm/conversation/', LLMConversationAPI.as_view(), name='llm-conversation'),
    path('llm/trending-questions/', TrendingQuestionsAPI.as_view(), name='llm-trending'),
]
