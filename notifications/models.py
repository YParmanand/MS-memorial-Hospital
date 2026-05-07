from django.db import models
from accounts.models import User
from appointments.models import Appointment


class Notification(models.Model):
    """SMS and notification system for patients and doctors"""
    
    NOTIFICATION_TYPE_CHOICES = (
        ('APPOINTMENT_CREATED', 'Appointment Created'),
        ('APPOINTMENT_APPROVED', 'Appointment Approved'),
        ('APPOINTMENT_REJECTED', 'Appointment Rejected'),
        ('APPOINTMENT_DELAYED', 'Appointment Delayed'),
        ('APPOINTMENT_CANCELLED', 'Appointment Cancelled'),
        ('APPOINTMENT_REMINDER', 'Appointment Reminder'),
        ('GENERAL', 'General Message'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES, default='GENERAL')
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_sms_sent = models.BooleanField(default=False)
    sms_status = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
