from django.db import models


class Service(models.Model):
    """Hospital services offered"""
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-eye', help_text='Font Awesome icon class')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Patient testimonials and reviews"""
    
    patient_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient_name} - {self.rating} stars"
