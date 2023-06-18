from django.urls import path
from .views import prescriptions, patient_info, approve_prescription, reject_prescription

app_name = 'pharmacist'

urlpatterns = [
    path("prescriptions", prescriptions, name="prescriptions"),
    path("approve_prescription/<int:prescription_id>",
         approve_prescription, name="approve_prescription"),
    path("reject_prescription/<int:prescription_id>",
         reject_prescription, name="reject_prescription"),
    path("patient_info/<int:patient_id>/", patient_info, name="patient_info"),
]
