from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count
from .models import FAQCategory, FAQItem
from .serializers import FAQCategorySerializer, FAQItemSerializer, FAQCategoryWithFAQsSerializer


class FAQListAPI(APIView):
    # Disable authentication for testing
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        category_id = request.query_params.get('categoryId')
        subcategory_id = request.query_params.get('subcategoryId')

        faqs = FAQItem.objects.all().select_related('category', 'subcategory')

        if category_id:
            faqs = faqs.filter(category_id=category_id)

        if subcategory_id:
            faqs = faqs.filter(subcategory_id=subcategory_id)

        serializer = FAQItemSerializer(faqs, many=True)
        return Response(serializer.data, status=200)


class FAQCategoriesAPI(APIView):
    # Disable authentication for testing
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        categories = FAQCategory.objects.prefetch_related('subcategories').annotate(
            subcategory_count=Count('subcategories')
        ).order_by('order', 'name')

        serializer = FAQCategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)

class FAQStaticTreeAPI(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # - 'faqs' → FAQ items directly under the category
        # - 'subcategories__faqs' → FAQ items under each subcategory
        categories = (
            FAQCategory.objects
            .prefetch_related(
                'faqs',
                'subcategories',
                'subcategories__faqs',
            )
            .order_by('order', 'name')
        )

        serializer = FAQCategoryWithFAQsSerializer(categories, many=True)
        return Response(serializer.data, status=200)

