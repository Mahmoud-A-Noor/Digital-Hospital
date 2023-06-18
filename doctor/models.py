from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Doctor(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    consultation_time = models.IntegerField(default=15, validators=[
        MinValueValidator(10),
        MaxValueValidator(45),
    ], null=True, blank=True)
    speciality = models.CharField(max_length=20, choices=DEPARTMENTS, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    years_of_expertise = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.email

    def get_full_timetable(self, day):
        return Timetable.objects.filter(doctor=self, day=day)

    def get_available_timetable(self, day):
        return Timetable.objects.filter(doctor=self, day=day, available=True)

DAYS = (
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
)

class Timetable(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )
    speciality = models.CharField(max_length=100, null=True, blank=True)
    day = models.CharField(max_length=9, choices=DAYS, null=True)
    time = models.TimeField(null=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.speciality:
            self.speciality = self.doctor.speciality
        super().save(*args, **kwargs)

    @staticmethod
    def get_specialty_timetable(speciality):
        return Timetable.objects.filter(speciality=speciality).values_list('doctor', flat=True)
    
    def __str__(self):
        return f"{self.day} - {self.time} - {self.available}"

class Pricing(models.Model):

    department = models.CharField(max_length=20, choices=DEPARTMENTS, null=True, blank=True)
    is_online = models.BooleanField()
    cost = models.IntegerField()

    class Meta:
        verbose_name = ("Pricing")
        verbose_name_plural = ("Pricing")

    def __str__(self):
        return f'{self.department}-{self.is_online}-{self.cost}'


