from django.db import models
from accounts.models import User


class Doctor(models.Model):
    """Doctor profile and information"""
    
    SPECIALIZATION_CHOICES = (
        ('GENERAL', 'General Ophthalmologist'),
        ('CATARACT', 'Cataract & Refractive Care'),
        ('RETINA', 'Vitreo Retina Specialist'),
        ('GLAUCOMA', 'Glaucoma Specialist'),
        ('OCULOPLASTY', 'Oculoplasty Specialist'),
        ('PEDIATRIC', 'Pediatric Ophthalmologist'),
        ('CORNEA', 'Cornea Specialist'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    registration_number = models.CharField(max_length=50, unique=True)
    bio = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    is_available = models.BooleanField(default=True)
    
    # Working hours
    monday_available = models.BooleanField(default=True)
    tuesday_available = models.BooleanField(default=True)
    wednesday_available = models.BooleanField(default=True)
    thursday_available = models.BooleanField(default=True)
    friday_available = models.BooleanField(default=True)
    saturday_available = models.BooleanField(default=True)
    sunday_available = models.BooleanField(default=False)
    
    start_time = models.TimeField(default='09:00:00')
    end_time = models.TimeField(default='17:00:00')
    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"
    
    @property
    def total_appointments(self):
        return self.appointments.count()
    
    @property
    def pending_appointments(self):
        return self.appointments.filter(status='PENDING').count()


class Gallery(models.Model):
    """Hospital and doctor images gallery"""
    
    CATEGORY_CHOICES = (
        ('HOSPITAL', 'Hospital'),
        ('DOCTOR', 'Doctor'),
        ('EQUIPMENT', 'Equipment'),
        ('FACILITY', 'Facility'),
        ('EVENT', 'Event'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='HOSPITAL')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
