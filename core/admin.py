from django.contrib import admin
from .models import StoreHours, SaleItem, AboutContent, Suggestion, StoreInfo
from django.utils.html import format_html

@admin.register(StoreHours)
class StoreHoursAdmin(admin.ModelAdmin):
    list_display = ['day', 'opening_time', 'closing_time', 'is_special_day', 'special_note']
    list_editable = ['opening_time', 'closing_time', 'is_special_day', 'special_note']
    ordering = ['day']
    fieldsets = (
        (None, {
            'fields': ('day', 'opening_time', 'closing_time', 'is_special_day', 'special_note'),
            'description': 'Edit store hours for each day. Use special note for holidays or exceptions.'
        }),
    )

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'original_price', 'is_active', 'created_at', 'image_tag']
    list_editable = ['price', 'original_price', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['image_tag']
    fields = ('title', 'description', 'price', 'original_price', 'image', 'image_tag', 'is_active')
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 120px;" />', obj.image.url)
        return ""
    image_tag.short_description = 'Image Preview'

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ['updated_at']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Only allow adding if there is no AboutContent
        return not AboutContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'suggestion']
    readonly_fields = ['created_at']

@admin.register(StoreInfo)
class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
