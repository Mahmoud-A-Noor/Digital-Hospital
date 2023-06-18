from django.db import models
from django.core.files.images import ImageFile
from django.contrib.auth import get_user_model
from doctor.models import Doctor, Timetable, Pricing
from pharmacist.models import Pharmacist
from os.path import basename
import datetime


class Patient(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    def get_open_requests(self):
        return Request.objects.filter(is_closed=False)

    def get_available_timetable(self, speciality):
        return Timetable.objects.filter(speciality=speciality, available=True)

    def create_appointment(self, request, doctor, timetable):
        try:
            Appointment.objects.create(
                patient=self,
                request=request,
                doctor=doctor,
                timetable=timetable,
            )
            timetable.available = False
            return True
        except:
            return False


def get_upload_path(instance, filename):
    return f'uploads/{instance.patient.user.id}/{filename}'


FILE_TYPES = (
    ('pdf', 'PDF'),
    ('image', 'Image'),
)


class Record(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_type = models.CharField(
        max_length=255, null=True, blank=True, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.file_name:  # Only set the filename if it's not already set
            self.file_name = basename(self.file.name)

        # Check if the file is a PDF or an image
        if not self.file_type:
            file_extension = self.file.name.split('.')[-1].lower()
            if file_extension == 'pdf':
                self.file_type = 'pdf'
            else:
                try:
                    ImageFile(self.file)
                    self.file_type = 'image'
                except Exception:
                    pass

        super().save(*args, **kwargs)


DEPARTMENTS = (
    ('cardiology', 'Cardiology'),
    ('dermatology', 'Dermatology'),
    ('gastroenterology', 'Gastroenterology'),
    ('neurology', 'Neurology'),
    ('orthopedics', 'Orthopedics'),
    ('pediatrics', 'Pediatrics'),
    ('psychiatry', 'Psychiatry'),
    ('urology', 'Urology'),
)


class Request(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=True, blank=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.PROTECT)
    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    complaint = models.TextField()
    online = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return F"{self.department} - {self.complaint[:15]}"

    def save(self, *args, **kwargs):
        if not self.department:
            self.department = self.doctor.speciality
        super().save(*args, **kwargs)

    @property
    def cost(self):
        return Pricing.objects.get(department=self.department, is_online=self.online).cost


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    date = models.DateField()
    is_finished = models.BooleanField(default=False)
    meeting_code = models.CharField(max_length=20, null=True, blank=True)

    @staticmethod
    def get_appointment_date(day, time_str):
        today = datetime.date.today()
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_index = days_of_week.index(day.lower())
        current_day_index = today.weekday()
        days_difference = (day_index - current_day_index) % 7
        target_date = today + datetime.timedelta(days=days_difference)
        
        current_datetime = datetime.datetime.now()
        chosen_time = datetime.datetime.strptime(time_str.strip(), "%H:%M:%S").time()
        chosen_datetime = datetime.datetime.combine(datetime.date.today(), chosen_time)
        
        if target_date < today or (target_date == today and chosen_datetime < current_datetime):
            target_date += datetime.timedelta(weeks=1)
        
        return target_date.strftime('%Y-%m-%d')
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = str(Appointment.get_appointment_date(self.timetable.day, str(self.timetable.time)))
        super().save(*args, **kwargs)


PRESCRIPTION_STATUS = (
    ("pendding", "Pendding"),
    ("approved", "Approved"),
    ("rejected", "Rejected")
)

class Prescription(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default="pendding", choices=PRESCRIPTION_STATUS)
    content = models.TextField(default="No Prescription by now")
    date = models.DateTimeField(auto_now_add=True)
    reject_reason = models.TextField(default="No Rejection")
    total_cost = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.patient.user.first_name} - {self.status}"

    @property
    def medication(self):
        return Medication.objects.filter(prescription=self)


class Medication(models.Model):

    drug_name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Medication")
        verbose_name_plural = ("Medication")

    def __str__(self):
        return self.drug_name