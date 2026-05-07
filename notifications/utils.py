"""
Notification utility functions for SMS and in-app notifications
"""
from django.utils import timezone
from .models import Notification


def send_notification(recipient, title, message, notification_type='GENERAL', sender=None, appointment=None):
    """
    Create and send notification to user
    
    Args:
        recipient: User object who will receive the notification
        title: Notification title
        message: Notification message content
        notification_type: Type of notification (default: GENERAL)
        sender: User object who sent the notification (optional)
        appointment: Related appointment object (optional)
    
    Returns:
        Notification object
    """
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        appointment=appointment,
        notification_type=notification_type,
        title=title,
        message=message,
    )
    
    # Simulate SMS sending (in production, integrate with Twilio/Fast2SMS)
    sms_sent = simulate_sms(recipient.phone, message)
    notification.is_sms_sent = sms_sent
    notification.sms_status = 'Sent (Simulated)' if sms_sent else 'Failed'
    notification.save()
    
    return notification


def simulate_sms(phone_number, message):
    """
    Simulate SMS sending (for development)
    In production, replace with actual SMS API integration
    """
    if phone_number:
        print(f"\n{'='*60}")
        print(f"SMS SENT TO: {phone_number}")
        print(f"MESSAGE: {message}")
        print(f"{'='*60}\n")
        return True
    return False


def send_appointment_notification(appointment, notification_type, custom_message=None):
    """
    Send appointment-related notification
    
    Args:
        appointment: Appointment object
        notification_type: Type of notification
        custom_message: Custom message (optional)
    """
    patient = appointment.patient
    doctor = appointment.doctor.user
    
    # Generate appropriate message based on notification type
    if notification_type == 'APPOINTMENT_CREATED':
        title = "Appointment Booked Successfully"
        message = custom_message or f"Your appointment with Dr. {doctor.get_full_name()} has been booked for {appointment.appointment_date} at {appointment.appointment_time}. Status: Pending approval."
    
    elif notification_type == 'APPOINTMENT_APPROVED':
        title = "Appointment Approved ✓"
        approved_date = appointment.approved_date or appointment.appointment_date
        approved_time = appointment.approved_time or appointment.appointment_time
        message = custom_message or f"Great news! Your appointment with Dr. {doctor.get_full_name()} has been approved for {approved_date} at {approved_time}. Please arrive 15 minutes early."
    
    elif notification_type == 'APPOINTMENT_REJECTED':
        title = "Appointment Update"
        reason = appointment.rejection_reason or "Doctor unavailable"
        message = custom_message or f"We regret to inform you that your appointment with Dr. {doctor.get_full_name()} could not be confirmed. Reason: {reason}. Please book another slot."
    
    elif notification_type == 'APPOINTMENT_DELAYED':
        title = "Appointment Rescheduled"
        approved_date = appointment.approved_date or appointment.appointment_date
        approved_time = appointment.approved_time or appointment.appointment_time
        message = custom_message or f"Your appointment with Dr. {doctor.get_full_name()} has been rescheduled to {approved_date} at {approved_time}. We apologize for the inconvenience."
    
    elif notification_type == 'APPOINTMENT_CANCELLED':
        title = "Appointment Cancelled"
        message = custom_message or f"Your appointment with Dr. {doctor.get_full_name()} scheduled for {appointment.appointment_date} has been cancelled."
    
    elif notification_type == 'APPOINTMENT_REMINDER':
        title = "Appointment Reminder"
        message = custom_message or f"Reminder: You have an appointment with Dr. {doctor.get_full_name()} tomorrow at {appointment.appointment_time}."
    
    else:
        title = "Appointment Update"
        message = custom_message or "Your appointment status has been updated."
    
    return send_notification(
        recipient=patient,
        title=title,
        message=message,
        notification_type=notification_type,
        sender=doctor,
        appointment=appointment
    )


def get_unread_count(user):
    """Get count of unread notifications for a user"""
    return Notification.objects.filter(recipient=user, is_read=False).count()


def mark_all_as_read(user):
    """Mark all notifications as read for a user"""
    notifications = Notification.objects.filter(recipient=user, is_read=False)
    for notification in notifications:
        notification.mark_as_read()
    return notifications.count()


# SMS API Integration (Optional - Uncomment and configure for production)
"""
# Example: Twilio Integration
from twilio.rest import Client

def send_sms_twilio(phone_number, message):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    twilio_number = 'your_twilio_number'
    
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)


# Example: Fast2SMS Integration
import requests

def send_sms_fast2sms(phone_number, message):
    api_key = 'your_fast2sms_api_key'
    url = 'https://www.fast2sms.com/dev/bulkV2'
    
    payload = {
        'authorization': api_key,
        'message': message,
        'numbers': phone_number,
        'route': 'v3',
        'sender_id': 'FSTSMS'
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return True, response.json()
        return False, response.text
    except Exception as e:
        return False, str(e)
"""
