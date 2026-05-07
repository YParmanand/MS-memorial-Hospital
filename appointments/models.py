from django.db import models
from accounts.models import User
from doctors.models import Doctor


class Appointment(models.Model):
    """Patient appointment booking and management"""
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DELAYED', 'Delayed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    problem_description = models.TextField()
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    admin_note = models.TextField(blank=True, null=True, help_text='Internal note for admin/doctor')
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Approved appointment details
    approved_date = models.DateField(blank=True, null=True)
    approved_time = models.TimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - Dr. {self.doctor.user.get_full_name()} ({self.status})"
    
    @property
    def is_pending(self):
        return self.status == 'PENDING'
    
    @property
    def is_approved(self):
        return self.status == 'APPROVED'
    
    @property
    def is_rejected(self):
        return self.status == 'REJECTED'


class Contact(models.Model):
    """Contact form submissions"""
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    reply_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
