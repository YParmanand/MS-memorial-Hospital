"""
MS Memorial Netralaya Hospital Website Setup Script
Run this script to set up the database and create sample data
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Doctor, Gallery
from core.models import Service, Testimonial
from accounts.models import Patient

User = get_user_model()

def create_superuser():
    """Create admin superuser"""
    print("\n=== Creating Superuser ===")
    if not User.objects.filter(email='admin@hospital.com').exists():
        User.objects.create_superuser(
            email='admin@hospital.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✓ Superuser created: admin@hospital.com / admin123")
    else:
        print("✓ Superuser already exists")


def create_chief_doctor():
    """Create Dr. Madhav Mukund as chief doctor"""
    print("\n=== Creating Chief Doctor ===")
    if not User.objects.filter(email='madhav@hospital.com').exists():
        doctor_user = User.objects.create_user(
            email='madhav@hospital.com',
            password='doctor123',
            first_name='Madhav',
            last_name='Mukund',
            role='DOCTOR',
            phone='+91-8004800688'
        )
        
        Doctor.objects.create(
            user=doctor_user,
            specialization='GENERAL',
            qualification='MBBS (KGMC Lucknow), MS (GSVM Kanpur)',
            experience_years=15,
            registration_number='UP-DOC-2008-001',
            bio='Dr. Madhav Mukund is a renowned ophthalmologist with extensive experience in comprehensive eye care. He earned his MBBS at King George Medical College (KGMC) in Lucknow and his MS at Ganesh Shankar Vidyarthi Memorial Medical (GSVM) College in Kanpur. With a wealth of knowledge and a well-earned reputation for delivering top-notch care, Dr. Mukund leads our team in improving the lives of patients across rural communities.',
            consultation_fee=500.00,
            is_available=True
        )
        print("✓ Chief Doctor created: Dr. Madhav Mukund")
    else:
        print("✓ Chief Doctor already exists")


def create_sample_doctors():
    """Create additional sample doctors"""
    print("\n=== Creating Sample Doctors ===")
    
    doctors_data = [
        {
            'email': 'kshitij@hospital.com',
            'first_name': 'Kshitij',
            'last_name': 'Aaditya',
            'phone': '+91-9876543210',
            'specialization': 'RETINA',
            'qualification': 'MBBS, DNB, FVRS (Retina), FICO (London), FRCS II (Glasgow)',
            'experience_years': 12,
            'registration_number': 'UP-DOC-2010-002',
            'bio': 'Senior Retina and ROP Specialist with international training.',
            'consultation_fee': 800.00
        },
        {
            'email': 'arvind@hospital.com',
            'first_name': 'Arvind',
            'last_name': 'Gautam',
            'phone': '+91-9876543211',
            'specialization': 'CATARACT',
            'qualification': 'MBBS, MS (Ophthalmology)',
            'experience_years': 10,
            'registration_number': 'UP-DOC-2012-003',
            'bio': 'Specialist in Cataract and Refractive Surgery.',
            'consultation_fee': 600.00
        }
    ]
    
    for doctor_data in doctors_data:
        if not User.objects.filter(email=doctor_data['email']).exists():
            doctor_user = User.objects.create_user(
                email=doctor_data['email'],
                password='doctor123',
                first_name=doctor_data['first_name'],
                last_name=doctor_data['last_name'],
                role='DOCTOR',
                phone=doctor_data['phone']
            )
            
            Doctor.objects.create(
                user=doctor_user,
                specialization=doctor_data['specialization'],
                qualification=doctor_data['qualification'],
                experience_years=doctor_data['experience_years'],
                registration_number=doctor_data['registration_number'],
                bio=doctor_data['bio'],
                consultation_fee=doctor_data['consultation_fee'],
                is_available=True
            )
            print(f"✓ Doctor created: Dr. {doctor_data['first_name']} {doctor_data['last_name']}")
        else:
            print(f"✓ Doctor already exists: Dr. {doctor_data['first_name']} {doctor_data['last_name']}")


def create_sample_patient():
    """Create sample patient"""
    print("\n=== Creating Sample Patient ===")
    if not User.objects.filter(email='patient@hospital.com').exists():
        patient_user = User.objects.create_user(
            email='patient@hospital.com',
            password='patient123',
            first_name='John',
            last_name='Doe',
            role='PATIENT',
            phone='+91-9876543212'
        )
        
        Patient.objects.create(
            user=patient_user,
            blood_group='O+',
            emergency_contact='+91-9876543213'
        )
        print("✓ Sample patient created: patient@hospital.com / patient123")
    else:
        print("✓ Sample patient already exists")


def create_services():
    """Create hospital services"""
    print("\n=== Creating Services ===")
    
    services_data = [
        {
            'title': 'Cataract & Refractive Care',
            'description': 'Clear vision, better life. Comprehensive cataract & refractive care with state-of-the-art technology.',
            'icon': 'fa-eye',
            'order': 1
        },
        {
            'title': 'Vitreo Retina Services',
            'description': 'Advanced vitreo-retina care. Expert specialists to preserve your vision with cutting-edge treatments.',
            'icon': 'fa-microscope',
            'order': 2
        },
        {
            'title': 'Glaucoma Services',
            'description': 'Comprehensive glaucoma care. Experienced specialists to protect your vision with advanced treatments.',
            'icon': 'fa-eye-dropper',
            'order': 3
        },
        {
            'title': 'Oculoplasty Services',
            'description': 'Enhance your eyes and face. Skilled oculoplasty specialists providing aesthetic & functional solutions.',
            'icon': 'fa-user-md',
            'order': 4
        }
    ]
    
    for service_data in services_data:
        Service.objects.get_or_create(
            title=service_data['title'],
            defaults=service_data
        )
    print("✓ Services created")


def create_testimonials():
    """Create patient testimonials"""
    print("\n=== Creating Testimonials ===")
    
    testimonials_data = [
        {
            'patient_name': 'Gopal Maurya',
            'message': 'I was here to get certified vision certificate for RRB\'s exam. Dr. Madhav Mukund (MBBS) is a man like humble and so polite in nature. I think you must visit once if you are facing eye related issues. One more thing what I want to tell you is that it is one of the best hospital in Zamania area.',
            'rating': 5
        },
        {
            'patient_name': 'Manvendra Singh',
            'designation': 'Social Worker',
            'message': 'Many congratulations and best wishes to you for providing world class eye care in Dildar Nagar, a small town of Ghazipur district.',
            'rating': 5
        },
        {
            'patient_name': 'Dr. C.D. Dwivedi',
            'designation': 'Medical Professional',
            'message': 'Superb clinic. You can\'t believe it that this type of grand ophtha setup in Dildarnagar. Even in Varanasi Eye hospital like this I have not seen. Dr. Madhav is very humble, polite and excellent in his expertise. I got operated my father\'s both eyes for cataract 2 years before. He is doing very well till date. Thank you very much Doctor. May god bless you.',
            'rating': 5
        },
        {
            'patient_name': 'Mukesh Singh',
            'message': 'Very much experienced and soft spoken eye doctor in Dildarnagar, Ghazipur. Must visit and avail the service by Dr Madhav Mukund and staff.',
            'rating': 5
        }
    ]
    
    for testimonial_data in testimonials_data:
        Testimonial.objects.get_or_create(
            patient_name=testimonial_data['patient_name'],
            defaults=testimonial_data
        )
    print("✓ Testimonials created")


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("MS MEMORIAL NETRALAYA HOSPITAL - DATABASE SETUP")
    print("="*60)
    
    try:
        create_superuser()
        create_chief_doctor()
        create_sample_doctors()
        create_sample_patient()
        create_services()
        create_testimonials()
        
        print("\n" + "="*60)
        print("✓ SETUP COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nDefault Login Credentials:")
        print("-" * 60)
        print("Admin:")
        print("  Email: admin@hospital.com")
        print("  Password: admin123")
        print("\nChief Doctor (Dr. Madhav Mukund):")
        print("  Email: madhav@hospital.com")
        print("  Password: doctor123")
        print("\nSample Patient:")
        print("  Email: patient@hospital.com")
        print("  Password: patient123")
        print("-" * 60)
        print("\nYou can now run: python manage.py runserver")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during setup: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
