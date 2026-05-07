from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Doctor, Gallery
from appointments.models import Appointment
from notifications.utils import send_appointment_notification


@login_required
def doctor_dashboard(request):
    """Doctor dashboard view"""
    
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Doctors only.')
        return redirect('core:home')
    
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please contact admin.')
        return redirect('core:home')
    
    # Get doctor's appointments
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-created_at')[:10]
    
    # Statistics
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    pending_appointments = Appointment.objects.filter(doctor=doctor, status='PENDING').count()
    approved_appointments = Appointment.objects.filter(doctor=doctor, status='APPROVED').count()
    rejected_appointments = Appointment.objects.filter(doctor=doctor, status='REJECTED').count()
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'rejected_appointments': rejected_appointments,
    }
    
    return render(request, 'doctors/doctor_dashboard.html', context)


@login_required
def appointment_list(request):
    """View all appointments for doctor"""
    
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Doctors only.')
        return redirect('core:home')
    
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('core:home')
    
    # Filter appointments
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = Appointment.objects.filter(doctor=doctor, status=status_filter).order_by('-created_at')
    else:
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-created_at')
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    
    return render(request, 'doctors/appointment_list.html', context)


@login_required
def appointment_action(request, appointment_id):
    """Approve, reject, or delay appointment"""
    
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Doctors only.')
        return redirect('core:home')
    
    try:
        doctor = request.user.doctor_profile
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('core:home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        custom_message = request.POST.get('custom_message', '')
        
        if action == 'APPROVED':
            appointment.status = 'APPROVED'
            appointment.approved_date = request.POST.get('approved_date') or appointment.appointment_date
            appointment.approved_time = request.POST.get('approved_time') or appointment.appointment_time
            appointment.save()
            
            # Send notification
            send_appointment_notification(appointment, 'APPOINTMENT_APPROVED', custom_message)
            messages.success(request, 'Appointment approved successfully!')
        
        elif action == 'REJECTED':
            appointment.status = 'REJECTED'
            appointment.rejection_reason = request.POST.get('rejection_reason', 'Doctor unavailable')
            appointment.save()
            
            # Send notification
            send_appointment_notification(appointment, 'APPOINTMENT_REJECTED', custom_message)
            messages.success(request, 'Appointment rejected.')
        
        elif action == 'DELAYED':
            appointment.status = 'DELAYED'
            appointment.approved_date = request.POST.get('approved_date')
            appointment.approved_time = request.POST.get('approved_time')
            appointment.save()
            
            # Send notification
            send_appointment_notification(appointment, 'APPOINTMENT_DELAYED', custom_message)
            messages.success(request, 'Appointment rescheduled successfully!')
        
        return redirect('doctors:appointment_list')
    
    context = {
        'appointment': appointment,
    }
    
    return render(request, 'doctors/appointment_action.html', context)


def doctor_list(request):
    """Public doctor list view"""
    
    # Filter by specialization
    specialization = request.GET.get('specialization', '')
    if specialization:
        doctors = Doctor.objects.filter(is_available=True, specialization=specialization)
    else:
        doctors = Doctor.objects.filter(is_available=True)
    
    context = {
        'doctors': doctors,
        'specialization_filter': specialization,
        'specializations': Doctor.SPECIALIZATION_CHOICES,
    }
    
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail(request, doctor_id):
    """Public doctor detail view"""
    
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    
    context = {
        'doctor': doctor,
    }
    
    return render(request, 'doctors/doctor_detail.html', context)


def gallery_view(request):
    """Gallery view"""
    
    category = request.GET.get('category', '')
    if category:
        images = Gallery.objects.filter(is_active=True, category=category).order_by('-created_at')
    else:
        images = Gallery.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'images': images,
        'category_filter': category,
        'categories': Gallery.CATEGORY_CHOICES,
    }
    
    return render(request, 'doctors/gallery.html', context)
