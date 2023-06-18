from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import phonenumbers
from accounts.models import CustomUser
from doctor.models import Doctor
from datetime import time
from .models import SystemAdmin
from main.decorators import user_type_required
from django.contrib import messages
from doctor.models import Doctor
from pharmacist.models import Pharmacist
from django.contrib.auth import get_user_model
from django.contrib import messages


def check_email_exists(email):
    User = get_user_model()
    return User.objects.filter(email=email).exists()


def check_phonenumber_exists(phone_number):
    User = get_user_model()
    return User.objects.filter(phone_number=phone_number).exists()


@login_required
@user_type_required("manager")
def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        img = request.FILES.get('img')
        user_type = "doctor"

        ### validate phone number ###
        try:
            phone_number = "+" + request.POST.get('country_code') + request.POST.get('phone_number')
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                exists = check_phonenumber_exists(phone_number)
                if exists:
                    messages.error(request, f'This phone number {phone_number} already associated with another account')
                    return redirect("system_admin:add_doctor")
            else:
                messages.error(request, 'Invalid phone number')
                return redirect('accounts:register')
        except:
            messages.error(request, 'Invalid phone number format')
            return redirect('accounts:register')

        ### check if email already exists ###
        exists = check_email_exists(email)
        if exists:
            messages.error(request, 'A user with the same email already exists')
            return redirect("system_admin:add_doctor")
        else:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                phone_number=phone_number,
                img=img,
                user_type=user_type,
            )


            doctor = Doctor.objects.get(user=user)
            consultation_time = int(request.POST.get("consultation_time"))

            doctor.consultation_time = consultation_time
            doctor.speciality = request.POST.get('specialty')
            doctor.years_of_expertise = request.POST.get('experience_years')
            doctor.bio = request.POST.get("bio")
            doctor.save()


            days = request.POST.getlist('days[]')
            hours_from = request.POST.getlist('hours_from[]')
            hours_to = request.POST.getlist('hours_to[]')

            SystemAdmin.create_doctor_timetable(days=days, start_hours=hours_from, end_hours=hours_to, consultation_time=consultation_time, doctor=doctor)
            
            return redirect("system_admin:doctors")
    return render(request, "dashboard/add_doctor.html")


@login_required
@user_type_required("manager")
def add_pharmacist(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        img = request.FILES.get('img')
        user_type = "pharmacist"

        ### validate phone number ###
        try:
            phone_number = "+" + request.POST.get('country_code') + request.POST.get('phone_number')
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                exists = check_phonenumber_exists(phone_number)
                if exists:
                    messages.error(request, f'This phone number {phone_number} already associated with another account')
                    return redirect("system_admin:add_pharmacist")
            else:
                messages.error(request, 'Invalid phone number')
                return redirect('accounts:register')
        except:
            messages.error(request, 'Invalid phone number format')
            return redirect('accounts:register')

        ### check if email already exists ###
        exists = check_email_exists(email)
        if exists:
            messages.error(request, 'A user with the same email already exists')
            return redirect("system_admin:add_pharmacist")
        else:
            CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                phone_number=phone_number,
                img=img,
                user_type=user_type,
            )
            return redirect("system_admin:pharmacists")
    return render(request, "dashboard/add_pharmacist.html")


@login_required
@user_type_required("manager")
def doctors(request):

    doctors = Doctor.objects.all()

    context = {
        "doctors": doctors,
    }

    return render(request, "dashboard/admin_doctors.html", context)


@login_required
@user_type_required("manager")
def delete_doctor(request, doctor_id):

    doctor = Doctor.objects.get(id=doctor_id)
    if doctor:
        CustomUser.objects.get(id=doctor.user.id).delete()
        messages.success(request, 'Doctor has been Deleted successfully.')
    else:
        messages.error(request, "Doctor couldn't be deleted.")

    return redirect("system_admin:doctors")


@login_required
@user_type_required("manager")
def pharmacists(request):

    pharmacists = Pharmacist.objects.all()

    context = {
        "pharmacists": pharmacists,
    }

    return render(request, "dashboard/admin_pharmacists.html", context)


@login_required
@user_type_required("manager")
def delete_pharmacist(request, pharmacist_id):

    pharmacist = Pharmacist.objects.get(id=pharmacist_id)
    if pharmacist:
        CustomUser.objects.get(id=pharmacist.user.id).delete()
        messages.success(request, 'Pharmacist has been Deleted successfully.')
    else:
        messages.error(request, "Pharmacist couldn't be deleted.")

    return redirect("system_admin:pharmacists")
