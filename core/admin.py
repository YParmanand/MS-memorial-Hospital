from django.contrib import admin
from .models import Service, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Service admin configuration"""
    
    list_display = ['title', 'icon', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Testimonial admin configuration"""
    
    list_display = ['patient_name', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['patient_name', 'message']
    date_hierarchy = 'created_at'
