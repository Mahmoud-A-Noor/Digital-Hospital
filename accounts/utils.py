import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import os

def send_otp(request):
    interval = 60 * 60
    timed_opt = pyotp.TOTP(pyotp.random_base32(), interval=interval)
    otp = timed_opt.now()
    time = datetime.now() + timedelta(seconds=interval)

    request.session['otp_secret_key'] = timed_opt.secret
    request.session['otp_validation_time'] = str(time)
    request.session['otp_interval'] = interval

    # Email configuration
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = request.session['email']
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'

    # Send the email
    send_mail(
        subject,
        message,
        sender_email,
        [receiver_email],
        fail_silently=False,
    )

    print(f'OTP is: {otp}')


def open_image_file(image_path):
    # Extract the file name and extension from the image path
    file_name = os.path.basename(image_path)
    file_ext = os.path.splitext(image_path)[1]

    # Read the image file from disk or storage
    with open(image_path, 'rb') as file:
        # Read the file content
        file_content = file.read()

    # Create an InMemoryUploadedFile object from the file content
    image_file = InMemoryUploadedFile(
        file=BytesIO(file_content),
        field_name=None,
        name=file_name,
        content_type=f'image/{file_ext}',  # Set the appropriate content type based on the file extension
        size=len(file_content),
        charset=None
    )
    
    return image_file