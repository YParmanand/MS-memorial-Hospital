from django import forms
from .models import Appointment, Contact
from doctors.models import Doctor


class AppointmentBookingForm(forms.ModelForm):
    """Appointment booking form for patients"""
    
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(is_available=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Doctor"
    )
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'problem_description']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'problem_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your eye problem in detail...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize doctor display
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.user.get_full_name()} - {obj.get_specialization_display()}"


class AppointmentActionForm(forms.ModelForm):
    """Form for doctor to approve/reject/delay appointments"""
    
    STATUS_CHOICES = (
        ('APPROVED', 'Approve'),
        ('REJECTED', 'Reject'),
        ('DELAYED', 'Delay/Reschedule'),
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )
    
    class Meta:
        model = Appointment
        fields = ['status', 'approved_date', 'approved_time', 'rejection_reason', 'admin_note']
        widgets = {
            'approved_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'approved_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for rejection (if applicable)'}),
            'admin_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Internal note (optional)'}),
        }


class ContactForm(forms.ModelForm):
    """Contact form for general inquiries"""
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }
