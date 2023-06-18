from django.urls import path
from .views import *

app_name = 'ai'

urlpatterns = [
    path('pneumonia/', pneumonia, name="pneumonia"),
    path('diabetic/', diabetic, name="diabetic"),
    path('brain_tumor/', brain_tumor, name="brain_tumor"),
]
