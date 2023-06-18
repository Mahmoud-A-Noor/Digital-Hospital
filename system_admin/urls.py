from django.urls import path
from .views import add_doctor, add_pharmacist, doctors, pharmacists, delete_doctor, delete_pharmacist

app_name = 'system_admin'

urlpatterns = [
    path('add_doctor/', add_doctor, name="add_doctor"),
    path('add_pharmacist/', add_pharmacist, name="add_pharmacist"),
    path('doctors/', doctors, name="doctors"),
    path('pharmacists/', pharmacists, name="pharmacists"),
    path('delete_doctor/<int:doctor_id>/', delete_doctor, name="delete_doctor"),
    path('delete_pharmacist/<int:pharmacist_id>/', delete_pharmacist, name="delete_pharmacist"),
]
