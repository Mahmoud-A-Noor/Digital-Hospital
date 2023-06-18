from django.shortcuts import render, redirect, get_object_or_404
from main.decorators import user_type_required
from django.contrib.auth.decorators import login_required
from patient.models import Prescription, Record, Patient, Pharmacist, Medication


@login_required
@user_type_required('pharmacist')
def prescriptions(request):

    pendding_prescription = Prescription.objects.filter(status="pendding")

    context = {
        'pendding_prescriptions': pendding_prescription,
    }

    return render(request, "dashboard/pharmacist_prescriptions.html", context=context)


@login_required
@user_type_required('pharmacist')
def approve_prescription(request, prescription_id):
    approved_prescription = Prescription.objects.get(pk=prescription_id)
    total_cost = request.POST.get('total')
    print(total_cost)
    approved_prescription.total_cost = total_cost

    approved_prescription.status = "approved"
    patient_request = approved_prescription.request
    patient_request.is_closed = True
    approved_prescription.save()
    patient_request.save()

    medicines = request.POST.getlist('medicine[]')
    medicines_prices = request.POST.getlist('price[]')

    for medicine, price in zip(medicines, medicines_prices):
        print(medicine)
        print(price)
        medication = Medication.objects.get(drug_name=medicine, prescription=approved_prescription)
        medication.cost = price
        medication.save()

    return redirect("pharmacist:prescriptions")


@login_required
@user_type_required('pharmacist')
def reject_prescription(request, prescription_id):
    # pharmacist = get_object_or_404(Pharmacist, user=request.user)
    # prescription = get_object_or_404(Prescription, pk=prescription_id)

    rejected_prescription = Prescription.objects.get(pk=prescription_id)
    rejected_prescription.status = "rejected"
    rejected_prescription.reject_reason = request.POST.get("complaint_content")

    # Complaint.objects.create(
    #     pharmacist=pharmacist, reject_reason=complaint_content, prescription=prescription)
    # print(Complaint.reject_reason)
    rejected_prescription.save()
    return redirect("pharmacist:prescriptions")


@login_required
@user_type_required('pharmacist')
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
