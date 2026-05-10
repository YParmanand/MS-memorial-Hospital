# MS Memorial Netralaya Hospital Website - Complete Setup Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- MySQL Server installed and running
- pip (Python package manager)
- Git (optional, for version control)

## Step-by-Step Installation

### 1. Database Setup

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Verify the database was created:
```sql
SHOW DATABASES;
```

### 2. Install Python Dependencies

Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.7
- mysqlclient (MySQL connector)
- Pillow (Image processing)
- django-crispy-forms (Form styling)
- crispy-bootstrap5 (Bootstrap 5 integration)
- python-decouple (Environment variables)

### 3. Configure Database Connection

The database settings are already configured in `hospital_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_db',
        'USER': 'root',
        'PASSWORD': 'parma123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**If your MySQL credentials are different**, update the settings.py file accordingly.

### 4. Run Database Migrations

Create all database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

You should see output showing all migrations being applied.

### 5. Create Sample Data

Run the setup script to create admin, doctors, patients, and sample data:

```bash
python setup.py
```

This will create:
- Admin user (admin@h*******.com / admin1**)
- Dr. Madhav Mukund (madhav@hospital.com / doctor123)
- Additional doctors
- Sample patient (patient@hospital.com / patient123)
- Hospital services
- Patient testimonials

### 6. Create Static Files Directory

```bash
python manage.py collectstatic --noinput
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The server will start at: http://localhost:8000/

## Access Points

### Public Pages
- **Homepage**: http://localhost:8000/
- **About**: http://localhost:8000/about/
- **Doctors**: http://localhost:8000/doctors/
- **Gallery**: http://localhost:8000/doctors/gallery/
- **Contact**: http://localhost:8000/appointments/contact/

### Authentication
- **Login**: http://localhost:8000/accounts/login/
- **Register**: http://localhost:8000/accounts/register/

### Admin Panel
- **URL**: http://localhost:8000/admin/
- **Credentials**: admin@h*******.com / admin1**

### Dashboards
- **Admin Dashboard**: http://localhost:8000/admin-dashboard/
- **Doctor Dashboard**: http://localhost:8000/doctors/dashboard/
- **Patient Dashboard**: http://localhost:8000/accounts/dashboard/

## Default User Accounts

### Admin
- **Email**: admin@h*******.com
- **Password**: admin1**
- **Access**: Full system control, analytics, user management

### Chief Doctor (Dr. Madhav Mukund)
- **Email**: madhav@hospital.com
- **Password**: doctor123
- **Access**: Appointment management, patient messages

### Sample Patient
- **Email**: patient@hospital.com
- **Password**: patient123
- **Access**: Book appointments, view history, notifications

## Testing the System

### 1. Test Patient Registration
1. Go to http://localhost:8000/accounts/register/
2. Fill in the registration form
3. Login with new credentials
4. Access patient dashboard

### 2. Test Appointment Booking
1. Login as patient
2. Click "Book Appointment"
3. Select doctor, date, time, and describe problem
4. Submit appointment

### 3. Test Doctor Approval
1. Logout and login as doctor (madhav@hospital.com)
2. Go to doctor dashboard
3. Click on pending appointment
4. Approve/Reject/Delay the appointment
5. Patient will receive notification

### 4. Test Notification System
1. Login as patient
2. Check notifications in dashboard
3. View all notifications
4. Check console for simulated SMS output

## Project Structure

```
hospital_project/
├── accounts/              # User authentication & profiles
│   ├── models.py         # User, Patient models
│   ├── views.py          # Login, register, dashboard views
│   ├── forms.py          # Registration, login forms
│   └── urls.py           # Account URLs
├── appointments/          # Appointment management
│   ├── models.py         # Appointment, Contact models
│   ├── views.py          # Booking, cancellation views
│   ├── forms.py          # Appointment forms
│   └── urls.py           # Appointment URLs
├── doctors/              # Doctor profiles & management
│   ├── models.py         # Doctor, Gallery models
│   ├── views.py          # Doctor dashboard, actions
│   └── urls.py           # Doctor URLs
├── core/                 # Core functionality & homepage
│   ├── models.py         # Service, Testimonial models
│   ├── views.py          # Home, about, admin dashboard
│   └── urls.py           # Core URLs
├── notifications/        # SMS & notification system
│   ├── models.py         # Notification model
│   ├── utils.py          # Notification functions
│   └── admin.py          # Notification admin
├── hospital_project/     # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── core/             # Homepage templates
│   ├── accounts/         # Auth templates
│   ├── doctors/          # Doctor templates
│   └── appointments/     # Appointment templates
├── static/              # CSS, JS, Images
│   ├── css/
│   │   └── custom.css   # Custom styles
│   ├── js/
│   └── images/
├── media/               # Uploaded files
│   ├── profiles/        # Profile pictures
│   └── gallery/         # Gallery images
├── requirements.txt     # Python dependencies
├── setup.py            # Database setup script
└── manage.py           # Django management script
```

## Key Features

### 1. User Authentication System
- Patient registration with email verification
- Role-based login (Admin, Doctor, Patient)
- Secure password hashing
- Profile management

### 2. Patient Dashboard
- View profile and appointments
- Book new appointments
- View appointment status
- Receive notifications
- View appointment history

### 3. Doctor Dashboard
- View all appointment requests
- Approve/Reject/Delay appointments
- Assign date and time slots
- Send messages to patients
- Manage availability

### 4. Admin Panel
- Add/edit/delete doctors
- Manage patients
- View all appointments
- Dashboard analytics
- Manage services and testimonials

### 5. Appointment System
- Select doctor, date, time
- Enter problem description
- Status flow: Pending → Approved/Rejected/Delayed
- Automatic notifications

### 6. Notification System
- In-app notifications
- SMS simulation (console output)
- Notification history
- Mark as read functionality

### 7. Contact System
- Contact form for inquiries
- Store messages in database
- Admin can view and respond

### 8. Gallery
- Hospital and doctor images
- Category-based filtering
- Responsive grid layout

## Customization

### Change Theme Colors

Edit `static/css/custom.css`:

```css
:root {
    --primary-color: #0066cc;      /* Change primary color */
    --secondary-color: #00a8e8;    /* Change secondary color */
    --accent-color: #4CAF50;       /* Change accent color */
}
```

### Add Real SMS Integration

1. Install Twilio:
```bash
pip install twilio
```

2. Update `notifications/utils.py` with your Twilio credentials:
```python
def send_sms_twilio(phone_number, message):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    twilio_number = 'your_twilio_number'
    # ... rest of the code
```

3. Replace `simulate_sms()` calls with `send_sms_twilio()`

### Change Background Image

Edit `static/css/custom.css`:

```css
.eye-background {
    background-image: url('your-image-url-here');
}
```

## Troubleshooting

### Issue: mysqlclient installation fails

**Solution**: 
- Windows: Download and install MySQL Connector from official MySQL website
- Linux: `sudo apt-get install python3-dev libmysqlclient-dev`
- Mac: `brew install mysql`

### Issue: Database connection error

**Solution**:
1. Verify MySQL is running
2. Check credentials in settings.py
3. Ensure database 'hospital_db' exists
4. Test connection: `mysql -u root -p`

### Issue: Static files not loading

**Solution**:
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Issue: Migrations error

**Solution**:
```bash
python manage.py makemigrations --empty accounts
python manage.py migrate --fake-initial
```

## Production Deployment

### Security Settings

Before deploying to production, update `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Enable security features
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Email Configuration

Configure SMTP for email notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Static Files for Production

```bash
python manage.py collectstatic
```

Configure your web server (Apache/Nginx) to serve static files.

## Support

For issues or questions:
- Check the troubleshooting section
- Review Django documentation: https://docs.djangoproject.com/
- Check MySQL documentation: https://dev.mysql.com/doc/

## License

Proprietary - MS Memorial Netralaya Hospital

---

**Congratulations! Your hospital website is now ready to use!** 🎉
