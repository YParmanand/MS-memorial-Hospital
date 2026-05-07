# MS Memorial Netralaya - Deployment Checklist

## Pre-Deployment Checklist

### 1. Database Setup ✓
- [ ] MySQL server installed and running
- [ ] Database `hospital_db` created
- [ ] Database user configured with proper permissions
- [ ] Database credentials updated in settings.py
- [ ] All migrations applied successfully
- [ ] Sample data loaded (optional)

### 2. Environment Configuration ✓
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed from requirements.txt
- [ ] Static files collected
- [ ] Media directories created with proper permissions

### 3. Security Settings ✓
- [ ] DEBUG = False in production
- [ ] SECRET_KEY changed to a secure random string
- [ ] ALLOWED_HOSTS configured with domain names
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] SECURE_SSL_REDIRECT = True
- [ ] Database password is strong and secure

### 4. Static & Media Files ✓
- [ ] STATIC_ROOT configured
- [ ] MEDIA_ROOT configured
- [ ] collectstatic command executed
- [ ] Web server configured to serve static files
- [ ] Media upload permissions set correctly

### 5. Email Configuration (Optional) ✓
- [ ] SMTP settings configured
- [ ] Email backend changed from console to SMTP
- [ ] Test email sent successfully
- [ ] Email credentials secured

### 6. SMS Integration (Optional) ✓
- [ ] SMS API credentials obtained (Twilio/Fast2SMS)
- [ ] SMS utility functions updated
- [ ] Test SMS sent successfully
- [ ] SMS credits/balance checked

### 7. Testing ✓
- [ ] All user registration flows tested
- [ ] Login/logout functionality verified
- [ ] Patient dashboard tested
- [ ] Doctor dashboard tested
- [ ] Admin dashboard tested
- [ ] Appointment booking tested
- [ ] Appointment approval/rejection tested
- [ ] Notification system tested
- [ ] Contact form tested
- [ ] Profile update tested
- [ ] All forms validated
- [ ] Error pages tested (404, 500)

### 8. Performance Optimization ✓
- [ ] Database queries optimized
- [ ] Images compressed
- [ ] CSS/JS minified (optional)
- [ ] Caching configured (optional)
- [ ] CDN configured for static files (optional)

### 9. Backup & Recovery ✓
- [ ] Database backup strategy in place
- [ ] Media files backup configured
- [ ] Backup restoration tested
- [ ] Automated backup scheduled

### 10. Monitoring & Logging ✓
- [ ] Error logging configured
- [ ] Access logs enabled
- [ ] Monitoring tools set up (optional)
- [ ] Alert system configured (optional)

## Production Settings Checklist

### settings.py Updates

```python
# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-server-ip']

# Secret Key (Generate new one)
SECRET_KEY = 'your-new-secret-key-here'

# Database (Production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_db',
        'USER': 'your_db_user',
        'PASSWORD': 'strong_password_here',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'MS Memorial Netralaya <noreply@yourdomain.com>'

# Static & Media Files
STATIC_ROOT = '/var/www/hospital/static/'
MEDIA_ROOT = '/var/www/hospital/media/'
```

## Server Configuration

### Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key
    
    # Django Application
    WSGIDaemonProcess hospital python-path=/path/to/hospital_project python-home=/path/to/venv
    WSGIProcessGroup hospital
    WSGIScriptAlias / /path/to/hospital_project/hospital_project/wsgi.py
    
    # Static Files
    Alias /static /var/www/hospital/static
    <Directory /var/www/hospital/static>
        Require all granted
    </Directory>
    
    # Media Files
    Alias /media /var/www/hospital/media
    <Directory /var/www/hospital/media>
        Require all granted
    </Directory>
    
    # Django Project
    <Directory /path/to/hospital_project/hospital_project>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location /static/ {
        alias /var/www/hospital/static/;
    }
    
    location /media/ {
        alias /var/www/hospital/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Deployment Commands

### 1. Prepare for Deployment

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser (if not exists)
python manage.py createsuperuser
```

### 2. Using Gunicorn (Recommended for Production)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn hospital_project.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Or create a systemd service
sudo nano /etc/systemd/system/hospital.service
```

### Systemd Service File

```ini
[Unit]
Description=MS Memorial Netralaya Hospital
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/hospital_project
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:/path/to/hospital.sock hospital_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Start Services

```bash
# Enable and start service
sudo systemctl enable hospital
sudo systemctl start hospital
sudo systemctl status hospital

# Restart web server
sudo systemctl restart apache2  # or nginx
```

## Post-Deployment Verification

### 1. Functionality Tests
- [ ] Homepage loads correctly
- [ ] All static files loading (CSS, JS, images)
- [ ] User registration works
- [ ] Login/logout works
- [ ] Patient can book appointment
- [ ] Doctor can approve appointment
- [ ] Notifications are sent
- [ ] Contact form works
- [ ] Admin panel accessible
- [ ] All pages responsive on mobile

### 2. Security Tests
- [ ] HTTPS working correctly
- [ ] HTTP redirects to HTTPS
- [ ] Admin panel requires authentication
- [ ] CSRF protection working
- [ ] SQL injection attempts blocked
- [ ] XSS attempts blocked

### 3. Performance Tests
- [ ] Page load time < 3 seconds
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Images loading quickly
- [ ] Server response time acceptable

## Maintenance Tasks

### Daily
- [ ] Check error logs
- [ ] Monitor server resources
- [ ] Check backup status

### Weekly
- [ ] Review appointment statistics
- [ ] Check contact messages
- [ ] Update content if needed

### Monthly
- [ ] Database optimization
- [ ] Security updates
- [ ] Backup verification
- [ ] Performance review

## Rollback Plan

If deployment fails:

1. **Database Rollback**
   ```bash
   python manage.py migrate app_name previous_migration_number
   ```

2. **Code Rollback**
   ```bash
   git checkout previous_stable_commit
   ```

3. **Restore Backup**
   ```bash
   mysql -u root -p hospital_db < backup.sql
   ```

## Support Contacts

- **Technical Support**: tech@msmemorialnetralaya.com
- **Database Admin**: dba@msmemorialnetralaya.com
- **Server Admin**: admin@msmemorialnetralaya.com

## Documentation Links

- Django Documentation: https://docs.djangoproject.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Bootstrap Documentation: https://getbootstrap.com/docs/

---

**Deployment Date**: _________________

**Deployed By**: _________________

**Verified By**: _________________

**Status**: ☐ Success ☐ Failed ☐ Partial

**Notes**: 
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
