from django.contrib import admin
from .models import Appointment, Contact


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Appointment admin configuration"""
    
    list_display = ['get_patient_name', 'get_doctor_name', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__email', 'doctor__user__first_name', 'doctor__user__last_name']
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'problem_description')
        }),
        ('Status & Response', {
            'fields': ('status', 'approved_date', 'approved_time', 'rejection_reason', 'admin_note')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        return obj.patient.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Contact message admin configuration"""
    
    list_display = ['name', 'email', 'subject', 'is_read', 'replied', 'created_at']
    list_filter = ['is_read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Response', {
            'fields': ('is_read', 'replied', 'reply_message')
        }),
    )
    
    readonly_fields = ['created_at']
