from django.db import models
from django.contrib.auth import get_user_model
from doctor.models import Timetable
from datetime import datetime, timedelta, time
from django.utils import timezone

# Create your models here.
class SystemAdmin(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("SystemAdmin")
        verbose_name_plural = ("SystemAdmins")

    def __str__(self):
        return self.user.email

    @staticmethod
    def create_doctor_timetable(days, start_hours, end_hours, consultation_time, doctor):
        current_date = timezone.now().date()
        current_weekday = current_date.weekday()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        for i, weekday in enumerate(days):
            weekday_index = (weekdays.index(weekday) - current_weekday + i * 7) % 7
            target_date = current_date + timedelta(days=weekday_index)

            start_hour = datetime.strptime(start_hours[i], '%H:%M').time()
            end_hour = datetime.strptime(end_hours[i], '%H:%M').time()

            start_time = datetime.combine(target_date, start_hour)
            end_time = datetime.combine(target_date, end_hour)
            current_time = start_time


            while current_time < end_time:
                timetable = Timetable()
                timetable.doctor = doctor
                timetable.day = weekday
                timetable.time = current_time.time()
                timetable.available = True
                timetable.save()

                current_time += timedelta(minutes=consultation_time)

                if current_time > end_time:
                    break

    ## this function handle when start time is greater than end time
    # @staticmethod
    # def create_doctor_timetable(days, start_hours, end_hours, consultation_time, doctor):
    #     current_date = timezone.now().date()

    #     weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    #     days_mapping = {day.lower(): day.capitalize() for day in weekdays}

    #     for i, target_weekday in enumerate(weekdays):
    #         if target_weekday.lower() in days:
    #             target_date = current_date + timedelta(days=(i - current_date.weekday() + 7) % 7)

    #             start_hour = datetime.strptime(start_hours[days.index(target_weekday.lower())], '%H:%M').time()
    #             end_hour = datetime.strptime(end_hours[days.index(target_weekday.lower())], '%H:%M').time()

    #             if start_hour <= end_hour:
    #                 start_time = datetime.combine(target_date, start_hour)
    #                 end_time = datetime.combine(target_date, end_hour)
    #             else:
    #                 # Handle case where appointment extends into the next day
    #                 start_time = datetime.combine(target_date, start_hour)
    #                 end_time = datetime.combine(target_date + timedelta(days=1), end_hour)

    #             current_time = start_time


    #             while current_time < end_time:
    #                 timetable = Timetable()
    #                 timetable.doctor = doctor
    #                 timetable.day = days_mapping[target_weekday.lower()]
    #                 timetable.time = current_time.time()
    #                 timetable.available = True
    #                 timetable.save()

    #                 current_time += timedelta(minutes=consultation_time)

    #                 if current_time > end_time:
    #                     break
