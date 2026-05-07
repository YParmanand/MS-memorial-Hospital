from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/action/', views.appointment_action, name='appointment_action'),
    path('gallery/', views.gallery_view, name='gallery'),
]
