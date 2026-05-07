# MS Memorial Netralaya Hospital Website

A modern, production-ready hospital management system built with Django.

## Features

- Patient Registration & Authentication
- Doctor Dashboard with Appointment Management
- Admin Panel for Complete Control
- SMS/Notification System
- Appointment Booking & Management
- Contact & Query System
- Gallery Management
- Responsive Bootstrap 5 Design

## Tech Stack

- **Backend**: Python, Django 4.2.7
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: MySQL
- **Architecture**: MVT (Model-View-Template)

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### 2. Database Setup

```sql
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Clone and Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample_data.json

# Run development server
python manage.py runserver
```

### 4. Access the Application

- **Homepage**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Patient Login**: http://localhost:8000/accounts/login/
- **Doctor Login**: http://localhost:8000/accounts/login/

## Default Credentials (After loading sample data)

### Admin
- Username: admin
- Password: admin123

### Doctor
- Email: doctor@hospital.com
- Password: doctor123

### Patient
- Email: patient@hospital.com
- Password: patient123

## Project Structure

```
hospital_project/
├── accounts/              # User authentication & profiles
├── appointments/          # Appointment management
├── doctors/              # Doctor profiles & management
├── core/                 # Core functionality & homepage
├── notifications/        # SMS & notification system
├── hospital_project/     # Main project settings
├── static/              # CSS, JS, Images
├── media/               # Uploaded files
└── templates/           # HTML templates
```

## Database Configuration

Edit `hospital_project/settings.py`:

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

## Key Features Explained

### User Roles
1. **Patient**: Book appointments, view history, receive notifications
2. **Doctor**: Manage appointments, send messages, view schedule
3. **Admin**: Full system control, analytics, user management

### Appointment Flow
1. Patient selects doctor and time slot
2. Status: Pending
3. Doctor reviews and approves/rejects/delays
4. Patient receives notification
5. Appointment confirmed with details

### Notification System
- All messages stored in database
- Visible in patient dashboard
- SMS simulation (can integrate real SMS API)

## Customization

### Adding Real SMS Integration

Install Twilio:
```bash
pip install twilio
```

Update `notifications/utils.py` with your Twilio credentials.

### Changing Theme Colors

Edit `static/css/custom.css` to modify color scheme.

## Security Features

- CSRF Protection
- Password Hashing (Django's built-in)
- Role-based Access Control
- Form Validation (Frontend + Backend)
- SQL Injection Prevention (Django ORM)

## Support

For issues or questions, contact the development team.

## License

Proprietary - MS Memorial Netralaya Hospital
