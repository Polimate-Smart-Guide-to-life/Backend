from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    IntegerField,
    JSONField,
)
from apps.lib.models import UUIDModel


class FAQCategory(UUIDModel):
    name = CharField(max_length=200, unique=True)
    icon = CharField(max_length=50, blank=True, null=True)
    description = TextField(blank=True, null=True)
    order = IntegerField(default=0)  # For ordering categories

    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class FAQSubcategory(UUIDModel):
    name = CharField(max_length=200)
    category = ForeignKey(FAQCategory, on_delete=CASCADE, related_name='subcategories')
    order = IntegerField(default=0)  # For ordering subcategories

    class Meta:
        verbose_name = "FAQ Subcategory"
        verbose_name_plural = "FAQ Subcategories"
        unique_together = [['category', 'name']]
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class FAQItem(UUIDModel):
    question = CharField(max_length=500)
    answer = TextField()
    category = ForeignKey(FAQCategory, on_delete=CASCADE, related_name='faqs')
    subcategory = ForeignKey(FAQSubcategory, on_delete=CASCADE, related_name='faqs', blank=True, null=True)
    tags = JSONField(default=list, blank=True)  # Array of strings - Django 5.1+ supports list as default
    views = IntegerField(default=0)
    helpful = IntegerField(default=0)
    order = IntegerField(default=0)  # For ordering within category/subcategory

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ['order', 'question']

    def __str__(self):
        return self.question

