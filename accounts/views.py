import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as builtin_login
from django.contrib.auth import logout as builtin_logout
from django.contrib import messages
from django.urls import reverse
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .utils import send_otp, pyotp, open_image_file
from datetime import datetime
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import phonenumbers
from django.contrib.auth import get_user_model



def check_email_exists(email):
    User = get_user_model()
    return User.objects.filter(email=email).exists()


def check_phonenumber_exists(phone_number):
    User = get_user_model()
    return User.objects.filter(phone_number=phone_number).exists()


@login_required
def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        img = request.FILES.get('img')


        user = CustomUser.objects.get(id=request.user.id)

        ### Validate email ###
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('accounts:profile')
        
        ### validate phone number ###
        try:
            phone_number = request.POST.get('phone_number')
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                exists = check_phonenumber_exists(phone_number)
                if exists:
                    messages.error(request, f'This phone number {phone_number} already associated with another account')
                    return redirect("accounts:profile")
                else:
                    user.phone_number = phone_number
            else:
                messages.error(request, 'Invalid phone number')
                return redirect('accounts:profile')
        except:
            messages.error(request, 'Invalid phone number format')
            return redirect('accounts:profile')
        
        # Check if old password matches
        if old_password:
            if user.check_password(old_password):
                if new_password:
                    user.set_password(new_password)
                else:
                    messages.error(request, "New password can't be empty")
                    return redirect('accounts:profile')
            else:
                messages.error(request, 'Old password is incorrect.')
                return redirect('accounts:profile')
        
       # Update user attributes
        if first_name:
            if first_name != user.first_name:
                user.first_name = first_name

        if last_name:
            if last_name != user.last_name:
                user.last_name = last_name

        if date_of_birth:
            if date_of_birth != user.date_of_birth:
                user.date_of_birth = date_of_birth

        # check if email already exists
        if email:
            if email != user.email and check_email_exists(email):
                messages.error(request, 'Email already exists.')
                return redirect('accounts:profile')
            else:
                user.email = email

        if address:
            if address != user.address:
                user.address = address

        if img:
            user.img = img
        
        user.save()
        
        messages.success(request, 'Your profile has been updated.')
        return redirect('accounts:profile')
    return render(request, 'profile.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            builtin_login(request, user)
            if user.user_type == "manager":
                return redirect('system_admin:doctors')
            elif user.user_type == "patient":
                return redirect('patient:requests')
            elif user.user_type == "doctor":
                return redirect('doctor:requests')
            elif user.user_type == "pharmacist":
                return redirect('pharmacist:prescriptions')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('accounts:login')
    
    return render(request, 'login.html')

@login_required
def logout(request):
    builtin_logout(request)
    return redirect(reverse('accounts:login'))

def register(request):
    if request.method == 'POST':
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['date_of_birth'] = request.POST.get('date_of_birth')
        request.session['gender'] = request.POST.get('gender')
        request.session['email'] = request.POST.get('email')
        request.session['address'] = request.POST.get('address')


        ### validate phone number ###
        try:
            phone_number = "+" + request.POST.get('country_code') + request.POST.get('phone_number')
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                exists = check_phonenumber_exists(phone_number)
                if exists:
                    messages.error(request, f'This phone number {phone_number} already associated with another account')
                    return redirect("accounts:profile")
                else:
                    request.session["phone_number"] = phone_number
            else:
                messages.error(request, 'Invalid phone number')
                return redirect('accounts:register')
        except:
            messages.error(request, 'Invalid phone number format')
            return redirect('accounts:register')

        ### check if email already exists ###
        exists = check_email_exists(request.POST.get('email'))
        if exists:
            messages.error(request, 'A user with the same email already exists')
            return redirect("accounts:register")

        ### store image and add path to session ###
        img_file = request.FILES.get('img')
        if img_file:
            filename = f'tmp_image_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg'
            request.session['img_path'] = default_storage.save('temp/' + filename, ContentFile(img_file.read()))            

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        request.session['password'] = request.POST.get('password')
        request.session['confirm_password'] = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')

        send_otp(request)

        return redirect('accounts:otp')
    
    return render(request, 'register.html')


def otp_view(request):
    if request.method == 'POST':

        otp = request.POST['otp']
        otp_secret_key = request.session['otp_secret_key']
        otp_validation_time = request.session['otp_validation_time']
        otp_interval = request.session['otp_interval']

        if otp_secret_key and otp_validation_time:
            otp_validation_time = datetime.fromisoformat(otp_validation_time)
            if otp_validation_time > datetime.now() and pyotp.TOTP(otp_secret_key, interval=otp_interval).verify(otp):
                del request.session['otp_secret_key']
                del request.session['otp_validation_time']

                first_name = request.session['first_name']
                last_name = request.session['last_name']
                date_of_birth = request.session['date_of_birth']
                gender = request.session['gender']
                email = request.session['email']
                password = request.session['password']
                address = request.session['address']
                phone_number = request.session["phone_number"]
                user_type = "patient"

                img = None
                img_path = request.session.get('img_path')
                if img_path:
                    full_img_path = default_storage.path(img_path)
                    img = open_image_file(full_img_path)

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
                
                if img_path:
                    default_storage.delete(img_path)

                builtin_login(request, user)

                return redirect('home')
            else:
                messages.error(request, 'OTP is incorrect.')
        else:
            messages.error(request, 'Something went wrong, try again!')

    return render(request, 'otp.html')