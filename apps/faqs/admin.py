from django.contrib import admin
from apps.faqs.models import FAQCategory, FAQSubcategory, FAQItem


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')


@admin.register(FAQSubcategory)
class FAQSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'order', 'name')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'subcategory', 'views', 'helpful', 'order', 'created_at')
    list_filter = ('category', 'subcategory')
    search_fields = ('question', 'answer')
    ordering = ('category', 'subcategory', 'order', 'question')

