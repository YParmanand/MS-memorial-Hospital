from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PatientRegistrationForm, UserLoginForm, ProfileUpdateForm, PatientProfileUpdateForm
from .models import User, Patient
from appointments.models import Appointment
from notifications.models import Notification


class PatientRegistrationView(CreateView):
    """Patient registration view"""
    
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please login to continue.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please check the form and try again.')
        return super().form_invalid(form)


def user_login(request):
    """User login view"""
    
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                
                # Redirect based on user role
                if user.is_admin:
                    return redirect('core:admin_dashboard')
                elif user.is_doctor:
                    return redirect('doctors:doctor_dashboard')
                else:
                    return redirect('accounts:patient_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def patient_dashboard(request):
    """Patient dashboard view"""
    
    if not request.user.is_patient:
        messages.error(request, 'Access denied. Patients only.')
        return redirect('core:home')
    
    # Get patient's appointments
    appointments = Appointment.objects.filter(patient=request.user).order_by('-created_at')[:10]
    
    # Get patient's notifications
    all_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    notifications = all_notifications[:10]
    unread_count = all_notifications.filter(is_read=False).count()
    
    # Statistics
    total_appointments = Appointment.objects.filter(patient=request.user).count()
    pending_appointments = Appointment.objects.filter(patient=request.user, status='PENDING').count()
    approved_appointments = Appointment.objects.filter(patient=request.user, status='APPROVED').count()
    
    context = {
        'appointments': appointments,
        'notifications': notifications,
        'unread_count': unread_count,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
    }
    
    return render(request, 'accounts/patient_dashboard.html', context)


@login_required
def profile_view(request):
    """User profile view and update"""
    
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if request.user.is_patient:
            patient_profile, created = Patient.objects.get_or_create(user=request.user)
            patient_form = PatientProfileUpdateForm(request.POST, instance=patient_profile)
            
            if user_form.is_valid() and patient_form.is_valid():
                user_form.save()
                patient_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        if request.user.is_patient:
            patient_profile, created = Patient.objects.get_or_create(user=request.user)
            patient_form = PatientProfileUpdateForm(instance=patient_profile)
        else:
            patient_form = None
    
    context = {
        'user_form': user_form,
        'patient_form': patient_form,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def notifications_view(request):
    """View all notifications"""
    
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark all as read
    if request.GET.get('mark_all_read'):
        notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('accounts:notifications')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'accounts/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a single notification as read"""
    
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.mark_as_read()
        messages.success(request, 'Notification marked as read.')
    except Notification.DoesNotExist:
        messages.error(request, 'Notification not found.')
    
    return redirect('accounts:notifications')
