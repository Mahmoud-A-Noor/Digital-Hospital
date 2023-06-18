from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from doctor.models import Doctor

class Command(BaseCommand):
    help = 'Create superusers'

    def handle(self, *args, **options):
        CustomUser.objects.create_superuser(
            email='manager@dj.dev',
            first_name='Super',
            last_name='Manager',
            date_of_birth='2002-01-12',
            gender='M',
            phone_number='01093577843',
            user_type='manager',
            password='rootroot'
        )
        
        CustomUser.objects.create_superuser(
            email='pharmacist@dj.dev',
            first_name='Super',
            last_name='Pharmacist',
            date_of_birth='2002-01-12',
            gender='M',
            phone_number='01093577843',
            user_type='pharmacist',
            password='rootroot'
        )

        CustomUser.objects.create_superuser(
            email='patient@dj.dev',
            first_name='Super',
            last_name='Patient',
            date_of_birth='2002-01-12',
            gender='M',
            phone_number='01093577843',
            user_type='patient',
            password='rootroot'
        )

        CustomUser.objects.create_superuser(
            email='doctor@dj.dev',
            first_name='Super',
            last_name='Doctor',
            date_of_birth='2002-01-12',
            gender='M',
            phone_number='01093577843',
            user_type='doctor',
            password='rootroot'
        )

        doctor = Doctor.objects.get(user__email='doctor@dj.dev')
        doctor.speciality = 'cardiology'
        doctor.save()