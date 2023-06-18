from django.urls import path
from .views import appointments, appointment_details, doctors, create_request, join_meeting, requests, medical_history, cancel_request, pay, delete_record, prescriptions, prescription_pay

app_name = 'patient'

urlpatterns = [
    path('requests/', requests, name="requests"),
    path('delete_request/<int:request_id>/', cancel_request, name='cancel_request'),
    path('appointments', appointments, name="appointments"),
    path('appointment_details/<int:appointment_id>/', appointment_details, name="appointment_details"),
    path('doctors/<str:speciality>/', doctors, name="doctors"),
    path('create_request', create_request, name="create_request"),
    path('medical_history', medical_history, name="medical_history"),
    path('delete_record/<int:record_id>/', delete_record, name="delete_record"),
    path('join_meeting/<int:appointment_id>/', join_meeting, name="join_meeting"),
    path('pay/', pay, name='payment'),
    path('prescriptions', prescriptions, name='prescriptions'),
    path('prescription_pay/<str:total_cost>/', prescription_pay, name='prescription_payment'),
]
