from django.contrib import admin
from .models import Doctor, Gallery


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Doctor admin configuration"""
    
    list_display = ['get_doctor_name', 'specialization', 'experience_years', 'is_available', 'consultation_fee']
    list_filter = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'registration_number']
    
    fieldsets = (
        ('Doctor Information', {
            'fields': ('user', 'specialization', 'qualification', 'experience_years', 'registration_number', 'bio', 'consultation_fee')
        }),
        ('Availability', {
            'fields': ('is_available', 'start_time', 'end_time')
        }),
        ('Working Days', {
            'fields': ('monday_available', 'tuesday_available', 'wednesday_available', 'thursday_available', 'friday_available', 'saturday_available', 'sunday_available')
        }),
    )
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor Name'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Gallery admin configuration"""
    
    list_display = ['title', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
