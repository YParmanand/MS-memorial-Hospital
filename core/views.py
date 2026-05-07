from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from doctors.models import Doctor, Gallery
from appointments.models import Appointment, Contact
from accounts.models import User
from .models import Service, Testimonial


def home(request):
    """Homepage view"""
    
    # Get featured doctors (limit to 3)
    doctors = Doctor.objects.filter(is_available=True)[:3]
    
    # Get services
    services = Service.objects.filter(is_active=True)[:4]
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    # Get gallery images
    gallery_images = Gallery.objects.filter(is_active=True)[:6]
    
    context = {
        'doctors': doctors,
        'services': services,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
    }
    
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    
    # Get all doctors for about page
    doctors = Doctor.objects.filter(is_available=True)
    
    context = {
        'doctors': doctors,
    }
    
    return render(request, 'core/about.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('core:home')
    
    # Statistics
    total_patients = User.objects.filter(role='PATIENT').count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='PENDING').count()
    approved_appointments = Appointment.objects.filter(status='APPROVED').count()
    rejected_appointments = Appointment.objects.filter(status='REJECTED').count()
    
    # Recent appointments
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:10]
    
    # Recent contacts
    recent_contacts = Contact.objects.filter(is_read=False).order_by('-created_at')[:5]
    
    # Appointment status breakdown
    appointment_stats = Appointment.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'rejected_appointments': rejected_appointments,
        'recent_appointments': recent_appointments,
        'recent_contacts': recent_contacts,
        'appointment_stats': appointment_stats,
    }
    
    return render(request, 'core/admin_dashboard.html', context)
