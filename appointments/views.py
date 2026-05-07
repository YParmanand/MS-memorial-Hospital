from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Contact
from .forms import AppointmentBookingForm, ContactForm
from notifications.utils import send_appointment_notification


@login_required
def book_appointment(request):
    """Book new appointment"""
    
    if not request.user.is_patient:
        messages.error(request, 'Only patients can book appointments.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = 'PENDING'
            appointment.save()
            
            # Send notification
            send_appointment_notification(appointment, 'APPOINTMENT_CREATED')
            
            messages.success(request, 'Appointment booked successfully! You will be notified once it is approved.')
            return redirect('accounts:patient_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentBookingForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'appointments/book_appointment.html', context)


@login_required
def appointment_detail(request, appointment_id):
    """View appointment details"""
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check permission
    if request.user != appointment.patient and not request.user.is_doctor and not request.user.is_admin:
        messages.error(request, 'You do not have permission to view this appointment.')
        return redirect('core:home')
    
    context = {
        'appointment': appointment,
    }
    
    return render(request, 'appointments/appointment_detail.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    """Cancel appointment"""
    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    if appointment.status in ['PENDING', 'APPROVED', 'DELAYED']:
        appointment.status = 'CANCELLED'
        appointment.save()
        
        # Send notification
        send_appointment_notification(appointment, 'APPOINTMENT_CANCELLED')
        
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')
    
    return redirect('accounts:patient_dashboard')


def contact_view(request):
    """Contact form view"""
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('core:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'appointments/contact.html', context)
