from django.urls import path
from .views import (appointments, requests, patient_info,
                    prescriptions, start_meeting,
                    update_prescription, add_prescription_appointment, add_prescriptions)

app_name = 'doctor'

urlpatterns = [
    path('requests', requests, name="requests"),
    path('appointments', appointments, name="appointments"),
    path('patient_info/<int:patient_id>/', patient_info, name="patient_info"),
    path('prescriptions', prescriptions, name="prescriptions"),
    path('add_prescriptions/<int:appointment_id>/', add_prescriptions, name="add_prescriptions"),
    #     path('show_complaints/<int:prescription_id>',
    #          show_complaints, name="show_complaints"),
    path('update_prescription/<int:prescription_id>',
         update_prescription, name="update_prescription"),
    path('start_meeting/<int:appointment_id>/',
         start_meeting, name="start_meeting"),
    #     path('approve_request/<int:request_id>/',
    #          approve_request, name="approve_request"),
    #     path('reject_request/<int:request_id>/',
    #          reject_request, name="reject_request"),
    path('add_prescription/<int:appointment_id>/',
         add_prescription_appointment, name="add_prescription")
]
