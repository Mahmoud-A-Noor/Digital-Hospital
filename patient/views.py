from django.shortcuts import redirect, render, get_object_or_404
from doctor.models import Doctor, Timetable, Pricing
from main.decorators import user_type_required
from django.contrib.auth.decorators import login_required
from .models import Patient, Request, Appointment, Prescription, Record, Medication
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
import stripe
from django.conf import settings

@login_required
@user_type_required('patient')
def requests(request):
    patient = get_object_or_404(Patient, user=request.user)
    patient_requests = Request.objects.filter(patient=patient)
    closed_requests = patient_requests.filter(is_closed=True).order_by('appointment__date', 'timetable__time')
    open_requests = patient_requests.filter(is_closed=False).order_by('appointment__date', 'timetable__time')

    context = {
        "open_requests": open_requests,
        "closed_requests": closed_requests,
    }

    return render(request, "dashboard/patient_requests.html", context)


@login_required
@user_type_required('patient')
def cancel_request(request, request_id):
    if request.method == "POST":
        patient_request = get_object_or_404(Request, pk=request_id)
        appointment = Appointment.objects.get(request=patient_request)

        if appointment.date == timezone.now().date():
            messages.error(request, "Sorry, Request can only be cancelled before the day of your appointment")
        else:

            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                cost = patient_request.cost * 100
                refund = stripe.Refund.create(
                    payment_intent=patient_request.payment_intent_id,
                    amount=cost,
                    reason='requested_by_customer'
                )
                # Check the refund status
                if refund.status == 'succeeded':
                    patient_request.status = 'refunded'
                    patient_request.save()
                    timetable = Timetable.objects.get(pk=patient_request.timetable.id)
                    timetable.available = True
                    timetable.save()
                    patient_request.delete()
                    messages.success(request, 'Your payment has been refunded.')

            except stripe.error.StripeError as e:
                messages.error(request, f'error: {e}')

        return redirect("patient:requests")
    else:
        return redirect("patient:requests")


@login_required
@user_type_required('patient')
def appointments(request):
    patient = get_object_or_404(Patient, user=request.user)
    all_appointments = Appointment.objects.filter(patient=patient)
    active_appointments = all_appointments.filter(is_finished=False).order_by("date", "timetable__time")
    previous_appointments = all_appointments.filter(is_finished=True).order_by("date", "timetable__time")

    context = {
        "active_appointments": active_appointments,
        "previous_appointments": previous_appointments,
    }

    return render(request, "dashboard/patient_appointments.html", context)


@login_required
@user_type_required('patient')
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    prescription = get_object_or_404(Prescription, request=appointment.request)

    context = {
        "appointment": appointment,
        "prescription": prescription
    }

    return render(request, "dashboard/patient_appointment_details.html", context)



@login_required
@user_type_required('patient')
def medical_history(request):
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == "POST":
        record_name = request.POST['record_name']
        record_date = request.POST['record_date']
        record_file = request.FILES['record_file']

        Record.objects.create(
            name=record_name, date=record_date, file=record_file, patient=patient)

    records = Record.objects.filter(patient=patient).order_by("date")

    context = {
        "patient": patient,
        "records": records
    }

    return render(request, "dashboard/patient_medical_history.html", context)


@login_required
@user_type_required('patient')
def delete_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    record.delete()
    return redirect("patient:medical_history")



@login_required
@user_type_required('patient')
def doctors(request, speciality):
    doctors = None
    selected_day = None
    online_cost = None
    onsite_cost = None

    if request.method == "POST":
        selected_day = request.POST.get('day')
        doctors = Doctor.objects.filter(
            speciality=speciality, timetable__day=selected_day, timetable__available=True).distinct()

    if selected_day is None:
        selected_day = datetime.now().strftime('%A').lower()
    if request.method == 'GET':
        doctors = Doctor.objects.filter(
            speciality=speciality, timetable__day=selected_day, timetable__available=True
        ).distinct()
        online_cost = Pricing.objects.get(department=speciality, is_online=True).cost
        onsite_cost = Pricing.objects.get(department=speciality, is_online=False).cost

    context = {
        "doctors": doctors,
        "selected_day": selected_day,
        "online_cost": online_cost,
        "onsite_cost": onsite_cost
    }

    return render(request, "dashboard/doctors.html", context)


@login_required
@user_type_required('patient')
def create_request(request):
    if request.method == "POST":
        request_type = True if request.POST.get(
            'request_type') == "online" else False
        day_working_time_id = request.POST.get('day_working_time')
        complaint = request.POST.get('complaint')

        timetable = Timetable.objects.get(pk=day_working_time_id)

        patient = Patient.objects.get(user=request.user)
        
        request.session['patient'] = patient.id
        request.session['doctor'] = timetable.doctor.id
        request.session['timetable'] = timetable.id
        request.session['complaint'] = complaint
        request.session['request_type'] = request_type


        return redirect("patient:payment")
    
    
    if request.method == "GET":
        day = request.GET.get("day")
        doctor_id = request.GET.get("doctor_id")
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        day_working_times = Timetable.objects.filter(day=day, doctor=doctor).order_by("time")
        online_cost = Pricing.objects.get(department=doctor.speciality, is_online=True).cost
        onsite_cost = Pricing.objects.get(department=doctor.speciality, is_online=False).cost

        context = {
            "doctor": doctor,
            "day_working_times": day_working_times,
            "online_cost": online_cost,
            "onsite_cost": onsite_cost
        }

        return render(request, "dashboard/create_request.html", context)

def pay(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        is_online = request.session['request_type']
        doctor = Doctor.objects.get(id=request.session['doctor'])
        department = doctor.speciality
        cost = Pricing.objects.get(department=department, is_online=is_online).cost
        amount = cost * 100

        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'token': token,
                },
            )

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                description='Example Payment',  # description will be customized later
                payment_method=payment_method.id,
                confirm=True
            )
            
            patient = Patient.objects.get(id=request.session['patient'])
            timetable = Timetable.objects.get(id=request.session['timetable'])
            complaint = request.session['complaint']

            patient_request = Request.objects.create(
                patient=patient,
                doctor=doctor,
                timetable=timetable,
                complaint=complaint,
                online=is_online,
                payment_intent_id=payment_intent.id
            )

            timetable.available = False
            timetable.save()

            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                timetable=timetable,
                request=patient_request
            )
            messages.success(request, 'Appointment created successfully.')
            return redirect("patient:requests")
        
        except stripe.error.CardError as e:
            messages.error(request, f'error: {e}')

    return render(request, 'payment.html', context={'url_name':'payment'})

@login_required
@user_type_required('patient')
def join_meeting(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if appointment.meeting_code:
        return render(request, 'dashboard/call.html', {"name": request.user.email, "meeting_code": appointment.meeting_code})
    else:
        messages.error(
            request, "Sorry, You can't join the meeting because the Doctor didn't start the meeting yet")
        return redirect('patient:appointments')

@login_required
@user_type_required('patient')
def prescriptions(request):
    patient = Patient.objects.get(user = request.user)
    prescriptions = Prescription.objects.filter(patient = patient)
    print(prescriptions)
    context = {
        'prescriptions': prescriptions,
    }
    return render(request, "dashboard/patient_prescriptions.html", context=context)

def prescription_pay(request, total_cost):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        from decimal import Decimal
        amount = int(Decimal(total_cost) * 100)

        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'token': token,
                },
            )

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                description='Example Payment',  # description will be customized later
                payment_method=payment_method.id,
                confirm=True
            )
            messages.success(request, 'Your order will be delivered soon!')
            return redirect("patient:prescriptions")
        
        except stripe.error.CardError as e:
            messages.error(request, f'error: {e}')

    return render(request, 'payment.html', context={'url_name':'prescription_payment', 'total_cost':total_cost})