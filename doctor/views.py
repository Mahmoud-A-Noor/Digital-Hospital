from django.shortcuts import render, redirect, get_object_or_404
from main.decorators import user_type_required
from django.contrib.auth.decorators import login_required
import random
from patient.models import Prescription, Appointment, Request, Patient, Record, Medication
from doctor.models import Timetable
from .models import Doctor
from django.utils import timezone


@login_required
@user_type_required('doctor')
def appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    all_appointments = Appointment.objects.filter(doctor=doctor)
    active_appointments = all_appointments.filter(is_finished=False).order_by('-date')
    # today = timezone.now().date()
    # active_appointments = active_appointments.filter(date=today)
    previous_appointments = all_appointments.filter(is_finished=True)

    context = {
        'active_appointments': active_appointments,
        'previous_appointments': previous_appointments,
    }
    return render(request, "dashboard/doctor_appointments.html", context)


@login_required
@user_type_required('doctor')
def requests(request):
    doctor = Doctor.objects.get(user=request.user)
    doctor_requests = Request.objects.filter(doctor=doctor)
    previous_requests = doctor_requests.filter(is_closed=True)
    pendding_requests = doctor_requests.filter(is_closed=False)

    context = {
        'previous_requests': previous_requests,
        'pendding_requests': pendding_requests,
        'doctor_id': doctor.id
    }

    return render(request, "dashboard/requests.html", context)


@login_required
@user_type_required('doctor')
def add_prescription_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    patient = appointment.patient
    appointement_request = appointment.request
    # appointement_request = get_object_or_404(Request, pk=request_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    prescription_content = request.POST.get("prescription_content")
    prescription = Prescription.objects.create(
        patient=patient,
        request=appointement_request,
        doctor=doctor,
        content=prescription_content
    )

    medicines = request.POST.getlist('medicine[]')
    print(medicines)
    for medicine in medicines:
        Medication.objects.create(drug_name=medicine, prescription=prescription)

    appointment.is_finished = True
    appointment.save()

    return redirect("doctor:appointments")


@login_required
@user_type_required('doctor')
def patient_info(request, patient_id):
    print(patient_id)
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        record_name = request.POST['record_name']
        record_date = request.POST['record_date']
        record_file = request.FILES['record_file']

        Record.objects.create(
            name=record_name, date=record_date, file=record_file, patient=patient)

    records = Record.objects.filter(patient=patient)

    context = {
        "patient": patient,
        "records": records
    }

    return render(request, "dashboard/patient_medical_history.html", context=context)


@login_required
@user_type_required('doctor')
def prescriptions(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    all_prescription = Prescription.objects.filter(doctor=doctor)
    pendding_prescription = all_prescription.filter(status="pendding")
    approved_prescription = all_prescription.filter(status="approved")
    rejected_prescription = all_prescription.filter(status="rejected")

    context = {
        'pendding_prescriptions': pendding_prescription,
        'approved_prescriptions': approved_prescription,
        'rejected_prescriptions': rejected_prescription,
    }
    return render(request, "dashboard/prescriptions.html", context=context)

@login_required
@user_type_required('doctor')
def add_prescriptions(request, appointment_id):
    return render(request, 'dashboard/doctor_add_prescription.html', context={'appointment_id': appointment_id})
# def show_complaints(request, prescription_id):
#     print("inside show complaints")
#     prescription = get_object_or_404(Prescription, pk=prescription_id)
#     complaint = Complaint.objects.filter(prescription=prescription)
#     print(complaint.reject_reason)

#     context = {
#         'complaint': complaint,
#     }

#     return render(request, "dashboard/prescriptions.html", context=context)

@login_required
@user_type_required('doctor')
def update_prescription(request, prescription_id):
    prescription_to_update = Prescription.objects.get(pk=prescription_id)
    prescription_to_update.content = request.POST.get("updated_content")
    prescription_to_update.status = "pendding"
    print(prescription_to_update.content)
    prescription_to_update.save()
    return redirect("doctor:prescriptions")

@login_required
@user_type_required('doctor')
def start_meeting(request, appointment_id):
    meeting_code = str(random.randint(0, 9999))

    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.meeting_code = meeting_code
    appointment.save()
    # * start meeting button in doctor_appointments.html must be configured to work with this function * #

    return render(request, 'dashboard/call.html', {"name": request.user.email, "meeting_code": meeting_code})
