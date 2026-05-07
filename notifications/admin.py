from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification admin configuration"""
    
    list_display = ['title', 'get_recipient_name', 'notification_type', 'is_read', 'is_sms_sent', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_sms_sent', 'created_at']
    search_fields = ['title', 'message', 'recipient__email', 'recipient__first_name', 'recipient__last_name']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'sender', 'appointment', 'notification_type', 'title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'is_sms_sent', 'sms_status')
        }),
    )
    
    readonly_fields = ['created_at', 'read_at']
    
    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name()
    get_recipient_name.short_description = 'Recipient'
