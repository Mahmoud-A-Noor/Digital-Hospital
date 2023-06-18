from django.http import HttpResponse
from django.shortcuts import render
from pharmacist.models import Notification

def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about-us.html')

def contact_us(request):
    return render(request, 'contact-us.html')

def brain_tumor_info(request):
    return render(request, 'brain_tumor_info.html')

def pneumonia_info(request):
    return render(request, 'pneumonia_info.html')

def diabetic_retinopathy_info(request):
    return render(request, 'diabetic_retinopathy_info.html')
    
def mark_user_notifications_as_read(request):
    Notification.mark_all_as_read(request.user.id)
    return HttpResponse(status=200)
