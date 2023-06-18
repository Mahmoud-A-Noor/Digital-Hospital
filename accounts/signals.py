from doctor.models import Doctor
from pharmacist.models import Pharmacist
from patient.models import Patient
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def create_user(instance, created, **kwargs):
    if created:
        user_type = instance.user_type
        if user_type == 'patient':
            Patient.objects.create(user = instance)
        elif user_type == "doctor":
            Doctor.objects.create(user = instance)
        elif user_type == "pharmacist":
            Pharmacist.objects.create(user = instance)
