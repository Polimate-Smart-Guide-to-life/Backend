from django.urls import path
from .views import FAQListAPI, FAQCategoriesAPI, FAQStaticTreeAPI

urlpatterns = [
    path('faqs/', FAQListAPI.as_view(), name='faq-list'),
    path('faqs/categories/', FAQCategoriesAPI.as_view(), name='faq-categories'),
    path('faqs/static/', FAQStaticTreeAPI.as_view(), name='faq-static'),
]