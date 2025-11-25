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

class FAQItemLiteSerializer(ModelSerializer):
    """
    Lightweight FAQ representation for the static FAQ endpoint.
    This is simpler than FAQItemSerializer:
    - No timestamps
    - No category/subcategory names
    - Intended for nested structures inside categories/subcategories
    """
    class Meta:
        model = FAQItem
        fields = ['id', 'question', 'answer', 'tags', 'order']
        read_only_fields = ['id']


class FAQSubcategoryWithFAQsSerializer(ModelSerializer):
    """
    Subcategory representation including the FAQ items belonging to it.
    Uses the related_name='faqs' defined in FAQItem.
    """
    faqs = FAQItemLiteSerializer(many=True, read_only=True)

    class Meta:
        model = FAQSubcategory
        fields = ['id', 'name', 'order', 'faqs']
        read_only_fields = ['id']


class FAQCategoryWithFAQsSerializer(ModelSerializer):
    """
    Complete static FAQ structure for a category:
    - FAQ items directly under the category (subcategory is NULL)
    - Subcategories with their own FAQ items
    """
    faqs = serializers.SerializerMethodField()
    subcategories = FAQSubcategoryWithFAQsSerializer(many=True, read_only=True)

    class Meta:
        model = FAQCategory
        fields = [
            'id',
            'name',
            'icon',
            'description',
            'order',
            'faqs',
            'subcategories',
        ]
        read_only_fields = ['id']

    def get_faqs(self, obj):
        """
        Returns FAQ items attached directly to the category
        (i.e., those with no subcategory assigned).
        """
        qs = obj.faqs.filter(subcategory__isnull=True).order_by('order', 'question')
        return FAQItemLiteSerializer(qs, many=True).data

