from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.faqs.models import FAQCategory, FAQSubcategory, FAQItem


class FAQSubcategorySerializer(ModelSerializer):
    categoryId = serializers.UUIDField(source='category.id', read_only=True)
    faqCount = serializers.SerializerMethodField()

    class Meta:
        model = FAQSubcategory
        fields = ['id', 'name', 'categoryId', 'faqCount']
        read_only_fields = ['id']

    def get_faqCount(self, obj):
        return obj.faqs.count()


class FAQCategorySerializer(ModelSerializer):
    subcategories = FAQSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'icon', 'description', 'subcategories']
        read_only_fields = ['id']


class FAQItemSerializer(ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    subcategory = serializers.CharField(source='subcategory.name', read_only=True, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = FAQItem
        fields = [
            'id',
            'question',
            'answer',
            'category',
            'subcategory',
            'tags',
            'views',
            'helpful',
            'createdAt',
            'updatedAt',
        ]
        read_only_fields = ['id', 'createdAt', 'updatedAt']

